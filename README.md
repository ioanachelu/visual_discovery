# visual_discovery

Steps to set up docker with elasticsearch:

* Install elasticsearch with ```pip install eleasticsearch```
* Install docker and docker-compose
* The vm.max_map_count kernel setting needs to be set to at least 262144. Follow this steps to set it:
    * Add  ```vm.max_map_count``` to ```/etc/sysctl.conf```
    * Run ```sysctl -w vm.max_map_count=262144```
* Run ```docker-compose up```
* Check in browser http://0.0.0.0:9200

* Delete index if any:

    ```curl -XDELETE http://localhost:9200/visual_discovery```
    
* Add index :

    ```curl -XPUT http://localhost:9200/visual_discovery -d @schema.json```  