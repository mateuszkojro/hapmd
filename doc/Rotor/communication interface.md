# Communication standard between Python API and C++ arduino software
|     *command*     | *shorthand* | *arguments* | *answer* | *response time* |          *example*          |                                             *description*                                              |
|:-----------------:|:-----------:|:-----------:|:--------:|:---------------:|:---------------------------:|:------------------------------------------------------------------------------------------------------:|
|     get angle     |     get     |     ---     |  float   |      short      |  req:'get' resp:'ok-12.4'   |                                          angle hold by rotor                                           |
|     set angle     |     set     |    float    |  float   |      long       | req:'set-12.4' resp:'-12.2' | the actual motor might not be able to turn to requested angle, the true angle set by rotor is returned |
| connection status |     con     |     ---     |   str    |      short      |   req:'con'    resp:'ok'    |                                         check connection state                                         |
