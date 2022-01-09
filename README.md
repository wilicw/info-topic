<div align="center">

# 大安高工資訊科專題網

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-vue.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/powered-by-oxygen.svg)](https://forthebadge.com)

> 大安高工資訊科學生專題製作展示與成果發表平臺。

</div>

## Demo

![](https://i.imgur.com/VahfqN5.png)

## Project's Structure

- `server` folder is for flask api.
- `ui` folder is for vuejs front-end pages.

| File | Function description |
|:----:|:---------------------|
| `docker-compose.yml` | Docker compose example file. |
| `Dockerfile` | Dockerfile for building container. |
| `makefile` | Makefile for building and configuring project. |
| `nginx.conf` | Production environment nginx config file. |
| `README.md` | This file. |
| `server/` | Flask api. |
| `ui/` | Vuejs front-end pages. |

### Server structure

| File | Function description |
|:----:|:---------------------|
| `config.ini` | Project config file. |
| `entities.py` | Config file parser, jwt processing, ranking, Chinese layout, file processing and validation functions. |
| `err.py` | Define several Http error messages. |
| `main.py` | Main file for flask server. | 
| `model.py` | Define database tables and columns. |
| `requirements.txt` | Pip requirements packages. |
| `startup.sh` | For docker container startup script. |
| `test_main.py` | Testing script. (incomplete) |
| `uwsgi.ini` | For production environment setting. |
| `resources/basic.py` | Blueprint for login, logout, change password and uploading files. |
| `resources/project.py` | Blueprint for project management and filtering. |
| `resources/ranking.py` | Blueprint for calculating projects' rank. |
| `resources/scores.py` | Blueprint for teachers to score projects. |
| `resources/ssr.py` | Blueprint for server side rendering preform better SEO. |
| `resiurces/students.py` | Blueprint for management students account. |
| `resources/teachers.py` | Blueprint for management teachers account. |
| `resources/years.py` | Blueprint for searching projects by year. |

### UI structure

| File | Function description |
|:----:|:---------------------|
| `public/` | Static files. |
| `src/` | Vuejs source files. |
| `configs.js` | Project config files. |
| `vue.config.js` | Vuejs config files. |
| `src/api.js` | Flask api interface. |
| `src/App.vue` | Vuejs main file. |
| `src/views/` | Vuejs pages. |
| `src/components/` | Vuejs components. |
| `src/router/` | Vuejs router. |
| `src/styles/` | Pages' stylesheet. |

## Configuration File

Server side config file is in `server/config.ini`. If you want to change it make sure you executed the test server on localhost before push into the production environment.

`ui/vue.config.js` and `ui/config.js` is the front-end config file. It contains `title`, `logo`, `url` and `authors`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Licence

```
Copyright 2021 William Chang

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
