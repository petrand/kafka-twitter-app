# Tweet Stream Analytics Dashboard

This application is designed to request, process and display a stream of tweets about specific topic (hashtag) from the Twitter API.

The dashboard shows life feed of tweets with side by side sentiment and key word analytics provided by pretrained [FinBERT](https://github.com/ProsusAI/finBERT) and [KeyBERT](https://github.com/MaartenGr/KeyBERT) models respectively. The dashboard is created using [Streamlit](https://streamlit.io/) UI designed for data apps


The application uses Kafka streams for intermediate storage of incoming tweets.

### Dashboard 
![Dashboard](/images/streamlit-app-2022-06-05-15-06-49_Trim.gif)
### Application Diagram
![Application Diagram](/images/app_diagram.png)

