# MyIMG

The image management system which supports S3.

## Installtion

Before installtion, prepare Python 3 and NodeJS.

```bash
git clone https://git.techo.cool/poormonitor/MyIMG.git myimg
cd myimg
pip install -r requirements.txt
cd view
npm install
npm run build
```

## Config

Touch `.env` in the main directory, and write the following information.

```dotenv
MYIMG_SECRET_KEY="{ generated by 'openssl rand -hex 32' }"
S3_ENDPOINT="s3.example.com"
S3_SECRET_ID=""
S3_SECRET_KEY=""
S3_REGION="ap-shanghai"
S3_BUCKET=""
S3_PREFIX="img"
S3_DOMAIN_PREFIX="https://assets.example.com"
REGISTER=1
```

## Run

Run the server by uvicorn.

```bash
uvicorn --port {Port} main:app
```

If you are running services on the system with systemd etc., you can touch the service file.

```
[Unit]
Description=MyIMG

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
User=www
PermissionsStartOnly=true
WorkingDirectory={Path to MyIMG}
ExecStart={Path to uvicorn} --port {Port} main:app
Restart=on-failure
TimeoutSec=600
```

Then, set nginx or other web servers to handle proxy to the port you set above.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Copyright

© 2022 Johnson Sun ([poormonitor@outlook.com](mailto:poormonitor@outlook.com)). All rights reserved.