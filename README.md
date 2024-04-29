# Nexus migrator asset file creator 
The "Nexus Migrator" tool mentioned in "Migrating from Sonatype Nexus Repository Manager to Artifactory > [Migrator Tool Overview](https://jfrog.com/help/r/jfrog-installation-setup-documentation/migrator-tool-overview)" has a  [migrateArtifact](https://jfrog.com/help/r/jfrog-installation-setup-documentation/run-the-migration-tool-in-multiple-stages) / ma option like:
```
./jfrog-nexus-migrator-<version>.sh ma --use-existing-asset-file="true" 
```

This `migrateArtifact` option expects a json file with a list of assets to migrate . Some customers generate this json file themselves , based on the `last_updated` date column in `raw_asset` table  , in the nexus database and pass it to the migrator tool .  Some use this approach only for the daily deltas ( after first initial full sync is completed) .


You can run the Postgres query like the following for a maven repository
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


Now convert it to a json asset file as below 
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
using the [nexus_list_to_json_migrator.py](nexus_list_to_json_migrator/nexus_list_to_json_migrator.py) as mentioned in 
[readme.md](nexus_list_to_json_migrator/readme.md)

Now use the in "Nexus Migrator" tool  with the  [migrateArtifact](https://jfrog.com/help/r/jfrog-installation-setup-documentation/run-the-migration-tool-in-multiple-stages) / `ma` option like:

```
./jfrog-nexus-migrator-<version>.sh ma --use-existing-asset-file="true" 
```

---

Or you can run a query like the following for multiple package types based on the `last_updated` date :

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