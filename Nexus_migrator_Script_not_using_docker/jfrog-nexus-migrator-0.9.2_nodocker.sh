#!/bin/bash

SCRIPT_LOCATION="/jfrog-nexus-migrator"
IMAGE_REPO="releases-docker.jfrog.io"
IMAGE_NAME="${IMAGE_REPO}/jfrog/jfrog-nexus-migrator"
IMAGE_TAG="0.9.2"
CONTAINER_DATA_LOCATION="/var/opt/jfrog/migrator/nexus"
MIGRATE_FLAG=""

currentDir=$(pwd)
workDir=${currentDir}/migration

check_command (){
  if [ $? -ne 0 ]; then
    printf "$1\n"
    exit 0
  fi
}

get_cli_home () {
  if [[ "$JFROG_CLI_HOME_DIR" == "" ]]; then
    JFROG_CLI_HOME=~/.jfrog
  else
    JFROG_CLI_HOME="$JFROG_CLI_HOME_DIR"
  fi
}

create_workdir(){
  mkdir $workDir
  check_command "[ERROR] : Failed creating $workDir. Check whether you have proper permissions."
  set_workdir
}

set_workdir(){
  get_cli_home
  JFROG_HOME="$workDir"
}

check_package (){
  $1 --version > /dev/null 2>&1
  check_command "[ERROR] : Unable to find $1 client in the PATH. Ensure that $1 is installed and added to the PATH."
}

display_help() {
    echo "Usage: ./migrate.sh [option]" >&2
    echo
    echo "   all, a                       Perform all migration activities in sequence "
    echo "   config, c                    Set configuration of Nexus Repository and Artifactory instances "
    echo "   getConfig, gc                Get repository and security configuration from Nexus Repository "
    echo "   createRepo, cr               Create repositories in Artifactory corresponding to those in Nexus Repository "
    echo "   migrateArtifact, ma          Migrate artifacts from Nexus Repository to Artifactory "
    echo "   migrateSecurity, ms          Migrate security entities from Nexus Repository to Artifactory "
    echo
    # echo some stuff here for the -a or --add-options
    echo "The following arguments are available only with options 'all' and 'config' "
    echo
    echo "To bypass Artifactory configuration through the command line : "
    echo "   --artifactoryUrl             JFrog Artifactory platform URL "
    echo "   --artifactoryUser            JFrog Artifactory username"
    echo "   --artifactoryPass            JFrog Artifactory password or API key"
    echo "To bypass Nexus configuration through the command line : "
    echo "   --nexusUrl                   Nexus Repository URL "
    echo "   --nexusUser                  Nexus Repository username "
    echo "   --nexusPass                  Nexus Repository password "
    echo "   --nexusDatadir               Nexus Repository data directory "
    echo "   --defaultPass                Default password in Artifactory for all the migrated users "
    echo
    echo "The following argument is available only with option 'migrateArtifact' "
    echo
    echo "   --threads                    Number of parallel worker threads to be used for Artifact Migration "
    echo "   --repos                      Migrate artifacts from given repositories (comma separated list) "
    echo "   --includePattern             Migrate artifacts from specific repository path (comma seperated list of folder patterns) [Only for nexus 3] "
    echo "   --check-binary-exists        Setting this option will skip the artifact migration if it exist on target [Only for nexus 3] "
    echo "   --force                      Setting this option will force run migration for repositories skipping the migration status of repositories [Only for nexus 3] "
    echo "   --print-failed-artifacts     Setting this option will print the list of artifacts which failed on migration [Only for nexus 3] "
    echo "   --use-existing-asset-file    Setting this option will use an existing asset file for artifact migration "
    echo "                                Make sure the file(<repo-name>_assetmap.json) is present in migration/nexus-migrator/ directory [Only for nexus 3]"
    echo
    exit 1
}

bannerStart() {
  title=$1
  echo
  echo -e "\033[1m${title}\033[0m"
  echo
}

docker_container_check() {
  process=$(docker ps | grep "jfrog-nexus-migrator" | wc -l | awk -F' ' '{print $1}')
  if [ "$process" != "0" ]; then
    printf "[ERROR] : Another migration process is in progress... \n[ERROR] : Either wait for the process to be complete or kill the container (docker kill jfrog-nexus-migrator)\n"
    exit 0
  else
    docker rm jfrog-nexus-migrator > /dev/null 2>&1
  fi
}

read_password() {
  password=""
  while IFS= read -r -n1 -s char; do
    case "$char" in
    $'\0')
        break
        ;;
    $'\177')
        if [ ${#password} -gt 0 ]; then
            echo -ne "\b \b"
            password=${password::-1}
        fi
        ;;
    *)
        chartCount=$((chartCount+1))
        echo -n '*'
        password+="$char"
        ;;
    esac
done
printf "\n"
}

# shellcheck disable=SC2120
readTerminalInput() {
repoList=""
IsArtInteractive=true
IsNexusInteractive=true
for i in "$@"; do
  case $i in
    --artifactoryUser=*)
      artifactoryUser="${i#*=}"
      ;;
    --artifactoryUrl=*)
      artifactoryUrl="${i#*=}"
      ;;
    --artifactoryPass=*)
      artifactoryPass="${i#*=}"
      ;;
    --nexusUrl=*)
      nexusUrl="${i#*=}"
      ;;
    --nexusUser=*)
      nexusUser="${i#*=}"
      ;;
    --nexusPass=*)
      nexusPass="${i#*=}"
      ;;
    --nexusDatadir=*)
      nexusDatadir="${i#*=}"
      ;;
    --defaultPass=*)
      defaultPass="${i#*=}"
      ;;
    --repos=*)
      repos="${i#*=}"
      ;;
    --includePattern=*)
      includePattern="${i#*=}"
      ;;
    --force=*)
      force="${i#*=}"
      ;;
    --print-failed-artifacts=*)
      printFailed="${i#*=}"
      ;;
    --check-binary-exists=*)
      checkBinary="${i#*=}"
      ;;
    --use-existing-asset-file=*)
      existingAssetFile="${i#*=}"
      ;;
    *)
      ;;
  esac
done
if [ -n "$artifactoryUrl" ] && [ -n "$artifactoryUser" ] && [ -n "$artifactoryPass" ]; then
  IsArtInteractive=false
fi

if [ -n "$nexusUrl" ] && [ -n "$nexusUser" ] && [ -n "$nexusPass" ] && [ -n "$nexusDatadir" ] && [ -n "$defaultPass" ]; then
  IsNexusInteractive=false
fi

if [ -n "$repos" ]; then
  repoList=$repos
fi

if [ -n "${includePattern}" ]; then
  includePatterns=${includePattern}
fi
}

readUserInputs() {
    readTerminalInput "$@"
    if [[ "$IsArtInteractive" == "true" ]]; then
      bannerStart "Configure Artifactory :"
      #docker run -it --name jfrog-nexus-migrator -v $JFROG_HOME:/root/.jfrog $IMAGE_NAME:$IMAGE_TAG jfrog c add
      jf c add
    else
      #docker run -it --name jfrog-nexus-migrator -v $JFROG_HOME:/root/.jfrog $IMAGE_NAME:$IMAGE_TAG jfrog c add artifactory --url="${artifactoryUrl}" --user="${artifactoryUser}" --password="${artifactoryPass}" --interactive=false
      jf c add artifactory --url="${artifactoryUrl}" --user="${artifactoryUser}" --password="${artifactoryPass}" --interactive=false
    fi
    check_command "[ERROR] : Failed to set Artifactory with JFrog CLI"
    SERVER_ID=$(cat $JFROG_HOME/jfrog-cli.conf.v6 | grep "serverId" | awk -F'"serverId":' '{print $2}' | awk -F'"' '{print $2}')
    if [[ "$IsNexusInteractive" == "true" ]]; then
      bannerStart "Configure Nexus Repository :"
      printf "Enter the Nexus Repository Data Directory : "
      read NEXUS_DATA
      printf "Enter the Nexus Repository URL : "
      read URL
      NEXUS_URL=$(echo $URL | sed 's/\/*$//g')
      printf "Enter the Nexus Repository username : "
      read NEXUS_USER
      printf "Enter the Nexus Repository password : "
      read_password
      NEXUS_PASS=$password
      printf "Enter a default password in Artifactory for all the migrated users : "
      read_password
      ART_PASS=$password
      printf "\n"
      extra_args="$SERVER_ID --nexus-workdir=$NEXUS_DATA --nexus-url=$NEXUS_URL --nexus-user=$NEXUS_USER --nexus-password=$NEXUS_PASS --default-password=$ART_PASS"
    else
      extra_args="$SERVER_ID --nexus-workdir=$nexusDatadir --nexus-url=$nexusUrl --nexus-user=$nexusUser --nexus-password=$nexusPass --default-password=$defaultPass"
    fi
}

docker_run() {
  if ! [ -d $workDir ]; then
    create_workdir
  fi
  set_workdir
  # if ! docker images | grep "$IMAGE_NAME" | grep " $IMAGE_TAG " | grep -v 'grep' &>/dev/null ; then
  #   docker pull $IMAGE_NAME:$IMAGE_TAG > /dev/null
  # fi
  command=$1
  extra_args=""
  if [ $command == "sc" ] || [ $command == "all" ]; then
    rm -rf $JFROG_HOME/jfrog-cli.conf* $JFROG_HOME/lock
    readUserInputs "$@"
    if [ ! -z "$nexusDatadir" ]; then
      NEXUS_DATA=$nexusDatadir
    fi
  else
    if [ $command == "ma" ]; then
      readTerminalInput "$@"
      if [ "$repoList" != "" ]; then
          extra_args="--repos=$repoList"
      fi
      if [ "$includePatterns" != "" ]; then
          extra_args="$extra_args --include-pattern=${includePatterns}"
      fi
      if [ "$force" == "true" ];then
          extra_args="$extra_args --force"
      fi
      if [ "$printFailed" == "true" ];then
          extra_args="$extra_args --print-failed-artifacts"
      fi
      if [ "$checkBinary" == "true" ];then
          extra_args="$extra_args --check-binary-exists"
      fi
      if [ "$existingAssetFile" == "true" ];then
          extra_args="$extra_args --use-existing-asset-file"
      fi
    fi
    configfile="$JFROG_HOME/nexus-migrator/migrationConfig.yaml"
    if [ -f "$configfile" ]; then
      datadir=$(grep "dataDir:" $configfile | tr -s ' ' | awk -F'dataDir:' '{print $2}'| tr -s ' '| sed 's/^ *//')
      if [ "$SKIP_MIGRATION_FILESYSTEM_CHECK" != true ];then
        if ! ( ([[ -d "$datadir/etc" ]] && [[ -d "$datadir/blobs" ]]) || ([[ -d "$datadir/conf" ]] && [[ -d "$datadir/storage" ]]) ); then
          printf "[ERROR] : Provide a valid Nexus Repository Data Directory\n"
          exit 1
        fi
      fi
      NEXUS_DATA=$(echo $datadir | tr -s ' ')
    else
      echo "[ERROR] :$configfile does not exist."
      exit 1
    fi
  fi
  # docker_container_check
  # docker run -i --name jfrog-nexus-migrator -e migratorLogLevel=${MIGRATOR_LOG_LEVEL} -e ENABLE_ASSET_PLUGIN="${ENABLE_ASSET_PLUGIN}" -v $JFROG_HOME:/root/.jfrog -v "$NEXUS_DATA":"$NEXUS_DATA" $IMAGE_NAME:$IMAGE_TAG jfrog-nexus-migrator $command $extra_args >> migration.log 2>&1 &
  env migratorLogLevel=${MIGRATOR_LOG_LEVEL} ENABLE_ASSET_PLUGIN="${ENABLE_ASSET_PLUGIN}" jfrog-nexus-migrator $command $extra_args >> migration.log 2>&1 &
  printf "Migration tool is running in background please check migration.log for details\n\n"
}

# check_package docker
check_package wc
check_package grep
check_package awk
# docker_container_check

if [ "$1" == "all" ] || [ "$1" == "a" ]; then
    bannerStart "Starting JFrog Nexus Migration [Full Migration]"
    MIGRATE_FLAG=sc:gc:cr:ma:ms
    docker_run all "$@"
elif [ "$1" == "config" ] || [ "$1" == "c" ]; then
    bannerStart "Starting JFrog Nexus Migration [Set Config]"
    MIGRATE_FLAG=sc
    docker_run sc "$@"
elif [ "$1" == "getConfig" ] || [ "$1" == "gc" ]; then
    bannerStart "Starting JFrog Nexus Migration [Get Nexus Config]"
    MIGRATE_FLAG=$MIGRATE_FLAG:gc
    docker_run gc
elif [ "$1" == "createRepo" ] || [ "$1" == "cr" ]; then
    bannerStart "Starting JFrog Nexus Migration [Create Repositories]"
    MIGRATE_FLAG=$MIGRATE_FLAG:cr
    docker_run cr
elif [ "$1" == "migrateArtifact" ] || [ "$1" == "ma" ]; then
    bannerStart "Starting JFrog Nexus Migration [Migrate Artifacts]"
    MIGRATE_FLAG=$MIGRATE_FLAG:ma
    docker_run ma "$@"
elif [ "$1" == "migrateSecurity" ] || [ "$1" == "ms" ]; then
    bannerStart "Starting JFrog Nexus Migration [Migrate Security Entities]"
    MIGRATE_FLAG=$MIGRATE_FLAG:ms
    docker_run ms
elif [ "$1" == "help" ] || [ "$1" == "-h" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ]; then
  display_help
else
  printf "[ERROR] : Invalid argument\n"
  display_help
fi