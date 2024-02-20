# Nexus migrator asset file creator 

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

This wull generate a list of artifact paths:

```
/testgp/tested/v12/testad-v12.jar
/testgp/tested/v12/testad-v12.jar.sha256
..
..
```

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
using the [nexus_list_to_json_migrator.py](nexus_list_to_json_migrator/nexus_list_to_json_migrator.py)

Or you can run a query like the following for multiple packahge types based on the `last_updated` date :

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
       AND a.last_updated > '"+str(sql_date)+"' ```

