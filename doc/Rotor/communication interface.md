# Communication standard between Python API and C++ arduino software
|     *command*     | *shorthand* | *arguments* | *answer* | *response time* |        *example*         |
|:-----------------:|:-----------:|:-----------:|:--------:|:---------------:|:------------------------:|
|     get angle     |     get     |     ---     |  float   |      short      | req:'get' resp:'ok-12.4' |
|     set angle     |     set     |    float    |   ---    |      long       | req:'set-12.4' resp:'ok' |
| connection status |     con     |     ---     |   str    |      short      |  req:'con'    resp:'ok'  |
