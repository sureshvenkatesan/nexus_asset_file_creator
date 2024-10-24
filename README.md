# Nexus migrator asset file creator 
The "Nexus Migrator" tool mentioned in "Migrating from Sonatype Nexus Repository Manager to Artifactory > [Migrator Tool Overview](https://jfrog.com/help/r/jfrog-installation-setup-documentation/migrator-tool-overview)" has a  [migrateArtifact](https://jfrog.com/help/r/jfrog-installation-setup-documentation/run-the-migration-tool-in-multiple-stages) / ma option like:
```
./jfrog-nexus-migrator-<version>.sh ma --use-existing-asset-file="true" 
```

This `migrateArtifact` option expects a json file with a list of assets to migrate . 

Some customers generate this json file themselves , based on the `last_updated` date column in `raw_asset` table  , in the nexus database and pass it to the migrator tool .  

Some use this approach only for the daily deltas ( after first initial full sync is completed) .

## Creating the asset json file:
### Postgres query for maven repository:

You can run the Postgres query like the following for a `maven` repository
to determine the files you are interested to migrate:

```
SELECT path
FROM   maven2_asset
WHERE  repository_id = (SELECT repository_id
                        FROM   maven2_content_repository
                        WHERE  config_repository_id =
                               (SELECT id
                                FROM   repository
                                WHERE  NAME = '<repo-name>')) ;
```

This will generate a list of artifact paths:

```
/testgp/tested/v12/testad-v12.jar
/testgp/tested/v12/testad-v12.jar.sha256
..
..
```
If you want the repo name also in the output you could modify the abovs sql as:
```
SELECT r.NAME AS repository_name, ma.path
FROM maven2_asset ma
JOIN maven2_content_repository mcr ON ma.repository_id = mcr.repository_id
JOIN repository r ON mcr.config_repository_id = r.id
WHERE r.NAME = '<repo-name>';
```

This query retrieves the repository name (r.NAME) along with the asset path (ma.path) from the maven2_asset table. It joins the maven2_content_repository table to link the asset to its repository using the repository_id, and then joins the repository table to get the name of the repository using the config_repository_id. Finally, it filters the results based on the repository name specified (r.NAME = '<repo-name>').


Using the [nexus_list_to_json_migrator.py](nexus_list_to_json_migrator/nexus_list_to_json_migrator.py) as mentioned in 
[readme.md](nexus_list_to_json_migrator/readme.md) convert it to a json asset file as below that can be used with 
the [Nexus migrator v 0.9.2](https://releases.jfrog.io/artifactory/run/nexus-migrator/0.9.2/jfrog-nexus-migrator-0.9.2.sh) .
```

 {
	"assets": [
		{
			"source": "SOURCE_REPO_NAME_IN_NEXUS/testgp/testad/v12/testad-v12.jar",
			"fileblobRef": ""
		},
		{
			"source": "SOURCE_REPO_NAME_IN_NEXUS/testgp/testad/v12/testad-v12.jar.sha256",
			"fileblobRef": ""
		},
        ..
        ...
    ]
}

```
For example if the source repo name in Nexus is `maven-releases` then the asset file contents will be:
```
{
	"assets": [
		{
			"source": "maven-releases/testgp/testad/v12/testad-v12.jar",
			"fileblobRef": ""
		},
		{
			"source": "maven-releases/testgp/testad/v12/testad-v12.jar.sha256",
			"fileblobRef": ""
		},
        ..
        ...
    ]
}

```
But with [Nexus migrator v 0.9.7](https://releases.jfrog.io/artifactory/run/nexus-migrator/0.9.7/jfrog-nexus-migrator-0.9.7.sh) it has
new improvements like the following, and  now the asset file  should have atleast sha1 or sha256  as requirted attributes:  
- Support for checksum validation of migrated Artifacts [INST-9100]. 
- Use Native checksum deploy API instead of head request check for `--check-binary-exists` [INST-9128]
So the new asset file format is:
Atleast one sha1 or sha256  i.e needs to be populated
```

 {
	"assets": [
		{
			"source": "SOURCE_REPO_NAME_IN_NEXUS/testgp/testad/v12/testad-v12.jar",
			"fileblobRef": ""
			"sha1": "sbcdefebed084ce239f85a81755add0cc3055e",
            "sha256": "abcdef042932cc8858d9df7f756841bf26b67335b53a281bc82f46ca9b062c"

		},
		{
			"source": "SOURCE_REPO_NAME_IN_NEXUS/testgp/testad/v12/testad-v12.jar.sha256",
			"fileblobRef": ""
			"sha1": "fe826077ebed084ce239f85a81755add0cc3055e",
            "sha256": "a901ee1c042932cc8858d9df7f756841bf26b67335b53a281bc82f46ca9b062c"

		},
        ..
        ...
    ]
}

```
---
### Postgres query for docker repository : 
```
SELECT path,
       attributes
FROM   docker_asset
WHERE  repository_id = (SELECT repository_id
                        FROM   docker_content_repository
                        WHERE  config_repository_id =
                               (SELECT id
                                FROM   repository
                                WHERE  NAME = '<repo-name>'));
```                                
Similary to the maven csv output , you can use the [docker_repo_csv_to_json_asset_file.py](docker_repo_csv_to_json_asset_file.py)
to covert the csv file to a docker asset json file  with format mentioned in next section.

### Sample docker asset file content for ver < 0.9.7: 
```
{
	"assets": {
		"blob": [
			{
				"source": "my-docker/v2/-/blobs/sha256:45c01c5d1f9c4b605692859d75b72c995131a6ec33257c8f1559aea43f896d8e",
				"fileblobRef": ""
			},
			{
				"source": "my-docker/v2/-/blobs/sha256:fbad7aa519f7da86dde82ab83e3130d8024e9ffebc315cead1fecb230e208340",
				"fileblobRef": ""
			},
			{
				"source": "my-docker/v2/-/blobs/sha256:daefd2028bfea420cf03362aef7e6758e57e979d75dc277cf6e176f0a72f51de",
				"fileblobRef": ""
			},
			{
				"source": "my-docker/v2/-/blobs/sha256:e2d17ec744c16f1ee6d8b676fec571faee36b16261d367670492aef4f72cfef9",
				"fileblobRef": ""
			}
		],
		"manifestV1": [
			{
				"source": "my-docker/v2/my-image/manifests/v1",
				"fileblobRef": "",
				"digest": "sha256:1f66ca0cd801f8c2b1b744f58376f08cfda584f491f7b03cd9f2d45d10f0738c"
			}
		],
		"manifestV2": [
			{
				"source": "my-docker/v2/my-image/manifests/sha256:1f66ca0cd801f8c2b1b744f58376f08cfda584f491f7b03cd9f2d45d10f0738c",
				"fileblobRef": "",
				"digest": "sha256:1f66ca0cd801f8c2b1b744f58376f08cfda584f491f7b03cd9f2d45d10f0738c"
			}
		]
	}
}
```

### Sample docker asset file content for ver >= 0.9.7: 
```
{
  "assets": {
    "blob": [
      {
        "source": "docker-hosted/v2/-/blobs/sha256:d0d53e58b36cb1c470ce93414129cb748daea358344026e1616b093d5771ea1b",
        "fileblobRef": "",
        "sha1": "eca0d4b9879cc2746f5880660257eb4693812216",
        "sha256": "d0d53e58b36cb1c470ce93414129cb748daea358344026e1616b093d5771ea1b"
      },
      {
        "source": "docker-hosted/v2/-/blobs/sha256:048743c919c1526b9fa80832977defc497b84b51d7a006c357754d1313a63bbb",
        "fileblobRef": "",
        "sha1": "f938ff246a8297175b7e2674f6e3a42fc3cea607",
        "sha256": "048743c919c1526b9fa80832977defc497b84b51d7a006c357754d1313a63bbb"
      },
      {
        "source": "docker-hosted/v2/-/blobs/sha256:25b7032c281a433b92d09930f3a03c0f7382c27eb69ae7f35addf2e3853dbba7",
        "fileblobRef": "",
        "sha1": "851bfb48fa5c4731c035eb8f26da6924c5339a3d",
        "sha256": "25b7032c281a433b92d09930f3a03c0f7382c27eb69ae7f35addf2e3853dbba7"
      },
      {
        "source": "docker-hosted/v2/-/blobs/sha256:af55c0d585657c73fc9bdbc6c1b78b08e6f59f52eb097b7ef4b9f468ccd7ec66",
        "fileblobRef": "",
        "sha1": "adb888cd96a94c5d29907e2efe7c55e2ce16a2da",
        "sha256": "af55c0d585657c73fc9bdbc6c1b78b08e6f59f52eb097b7ef4b9f468ccd7ec66"
      },
      {
        "source": "docker-hosted/v2/-/blobs/sha256:97e04611ad43405a2e5863ae17c6f1bc9181bdefdaa78627c432ef754a4eb108",
        "fileblobRef": "",
        "sha1": "06190fdb84783e97b1524d6ade40e3014b005835",
        "sha256": "97e04611ad43405a2e5863ae17c6f1bc9181bdefdaa78627c432ef754a4eb108"
      }
    ],
    "manifestV1": [
      {
        "source": "docker-hosted/v2/rancher-desktop/rdx-proxy/manifests/v1",
        "fileblobRef": "",
        "digest": "sha256:1c3e6f113fefa7581e3103687561b80db5896eb0895c784f589509bfc3aeed55",
        "sha1": "e0544abd30b3e3037a271056d0f206f12bcd3645",
        "sha256": "1c3e6f113fefa7581e3103687561b80db5896eb0895c784f589509bfc3aeed55"
      },
      {
        "source": "docker-hosted/v2/coredns-coredns/manifests/1.10.1",
        "fileblobRef": "",
        "digest": "sha256:74130b944396a0b0ca9af923ee6e03b08a35d98fc1bbaef4e35cf9acc5599105",
        "sha1": "3b9e8f2a15af27e353a05eabc45d91e996e034a6",
        "sha256": "74130b944396a0b0ca9af923ee6e03b08a35d98fc1bbaef4e35cf9acc5599105"
      }
    ],
    "manifestV2": [
      {
        "source": "docker-hosted/v2/rancher-desktop/rdx-proxy/manifests/sha256:1c3e6f113fefa7581e3103687561b80db5896eb0895c784f589509bfc3aeed55",
        "fileblobRef": "",
        "digest": "sha256:1c3e6f113fefa7581e3103687561b80db5896eb0895c784f589509bfc3aeed55",
        "sha1": "e0544abd30b3e3037a271056d0f206f12bcd3645",
        "sha256": "1c3e6f113fefa7581e3103687561b80db5896eb0895c784f589509bfc3aeed55"
      },
      {
        "source": "docker-hosted/v2/coredns-coredns/manifests/sha256:74130b944396a0b0ca9af923ee6e03b08a35d98fc1bbaef4e35cf9acc5599105",
        "fileblobRef": "",
        "digest": "sha256:74130b944396a0b0ca9af923ee6e03b08a35d98fc1bbaef4e35cf9acc5599105",
        "sha1": "3b9e8f2a15af27e353a05eabc45d91e996e034a6",
        "sha256": "74130b944396a0b0ca9af923ee6e03b08a35d98fc1bbaef4e35cf9acc5599105"
      }
    ]
  }
}
```

### Special Notes :- 

Docker repository consist of mainly 3 types of artifacts in nexus repository.

Docker layers (which will be stored under <repo-name>/v2/-/blobs/ )  →  assets.blob
Docker manifest file under version tag (which will be stored under <repo-name>/v2/<image-name>/manifests/<tag>)  → assets.manifestV1
Docker manifest file with digest value (which will be stored under <repo-name>/v2/<image-name>/manifests/) → assets.manifestV2

---

Once you have the asset json file , use the in "Nexus Migrator" tool mentioned in "Migrating from Sonatype Nexus Repository Manager to Artifactory > [Migrator Tool Overview](https://jfrog.com/help/r/jfrog-installation-setup-documentation/migrator-tool-overview)" with the the [migrateArtifact](https://jfrog.com/help/r/jfrog-installation-setup-documentation/run-the-migration-tool-in-multiple-stages) / `ma` option like:

```
./jfrog-nexus-migrator-<version>.sh ma --use-existing-asset-file="true" 
```

**Note:** If the source repo in Nexus is named `maven-releases` and the target repo in Artifactory is `maven-releases-local` the name of the asset file shoule be `<targetrepo-name>_assetmap.json` .

For example: `maven-releases-local_assetmap.json`

---

You can run a query like the following for multiple package types based on the `last_updated` date :

```
SELECT r.NAME AS Repo_Name,
       a.path
FROM   repository r
       JOIN yum_content_repository cr
         ON cr.config_repository_id = r.id
       LEFT OUTER JOIN yum_component c
                    ON c.repository_id = cr.repository_id
       LEFT OUTER JOIN yum_asset a
                    ON c.component_id = a.component_id
WHERE  recipe_name LIKE '%hosted'
       AND a.last_updated > '" +str(sql_date)+ "'
UNION ALL
SELECT r.NAME AS Repo_Name,
       a.path
FROM   repository r
       JOIN raw_content_repository cr
         ON cr.config_repository_id = r.id
       LEFT OUTER JOIN raw_component c
                    ON c.repository_id = cr.repository_id
       LEFT OUTER JOIN raw_asset a
                    ON c.component_id = a.component_id
WHERE  recipe_name LIKE '%hosted'
       AND a.last_updated > '"+str(sql_date)+"' 
```
Then you can use the  [Nexus_multi_repos_DeltaSync_from_date.py](Nexus_multi_repos_DeltaSync_from_date/Nexus_multi_repos_DeltaSync_from_date.py) script as mentioned in [readme.md](Nexus_multi_repos_DeltaSync_from_date/readme.md)

---

You could also potentially make a few optimizations such as using INNER JOIN instead of LEFT OUTER JOIN `if applicable`
and ensure that necessary indexes are present on columns used in join conditions (config_repository_id, repository_id, component_id).
```
SELECT r.NAME AS Repo_Name,
       a.path
FROM   repository r
       JOIN yum_content_repository cr
         ON cr.config_repository_id = r.id
       JOIN yum_component c
         ON c.repository_id = cr.repository_id
       JOIN yum_asset a
         ON c.component_id = a.component_id
WHERE  recipe_name LIKE '%hosted'
       AND a.last_updated > '" + str(sql_date) + "'
UNION ALL
SELECT r.NAME AS Repo_Name,
       a.path
FROM   repository r
       JOIN raw_content_repository cr
         ON cr.config_repository_id = r.id
       JOIN raw_component c
         ON c.repository_id = cr.repository_id
       JOIN raw_asset a
         ON c.component_id = a.component_id
WHERE  recipe_name LIKE '%hosted'
       AND a.last_updated > '" + str(sql_date) + "';
```
---
