![Background image](https://i.ibb.co/HBxv8Tp/analyzecctv.webp)

# Real-time CCTV footage analysis with AI
The program utilizes OpenCV to capture snapshots from the camera feed, which are then analyzed by a pre-trained AI model (YOLOv10n). If the model detects a person in the image, the program automatically sends an alert to a designated Telegram chat.

## Requirements
- Docker
- Telegram

## How to use it?
### Step 1: Create a Configuration File
You need to create a `config.json` file that contains a list of cameras with their names and RTSP URLs. Below is an example configuration with three cameras:

```json
{
    "cameras": [
        {
            "name": "Driveway",
            "url": "rtsp://172.16.0.10/stream"
        },
        {
            "name": "Backyard",
            "url": "rtsp://172.16.0.11/stream"
        },
        {
            "name": "Door",
            "url": "rtsp://172.16.0.12/stream"
        }
    ]
}
```

### Step 2: Set Up Telegram Bot
1. **Create a Bot:** Open Telegram and talk to [@BotFather](https://t.me/BotFather). Follow the instructions to create a new bot and get your bot token.
2. **Get Chat ID:**
   - Send a message to your newly created bot.
   - Open your browser and visit:  
     `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`  
     Replace `<YOUR_TOKEN>` with the token you received from @BotFather.
   - You will receive a JSON response. Look for the following part to find your chat ID:
     ```json
     "chat": {
         "id": 12345678,
     ```

### Step 3: Start the Docker Container
Run the following command to start the container:
```bash
docker run -d --name analyzecctv \
-v /path/to/config.json:/app/config.json \
-e TG_TOKEN=YOUR_TOKEN \
-e TG_CHAT_ID=YOUR_CHAT_ID \
--restart always \
aleksandergpl/analyzecctv
```

Replace `/path/to/config.json` with the actual path to your configuration file. Additionally, substitute `YOUR_TOKEN` and `YOUR_CHAT_ID` with your bot’s token and chat ID.


## Enviromental variables:
- `DELAY` - Delay between checking the camera feed
- `CONF_TRESH` - Confidence treshold for the AI model
- `TG_TOKEN` - Telegram bot token 
- `TG_CHAT_ID` - Telegram chat id