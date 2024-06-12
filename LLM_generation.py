import openai
import os
import csv
import json
import pandas as pd
import sys
import random

openai.api_type = "azure"
openai.api_base = "insert_yours" # TODO
openai.api_version = "2023-09-01-preview"
openai.api_key = "insert_yours" # TODO

def get_completion_from_messages(messages):
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=messages,
        temperature=1,
        top_p=1
    )
    response_content = response.choices[0].message["content"]
    return response_content


language = sys.argv[1]
counts_dirs = {'English': "data/counts/real_English.csv", 'Chinese': "data/counts/real_Chinese.csv",
               'Romanian': "data/counts/real_Romanian.csv", 'Russian': "data/counts/real_Russian.csv",
               'Spanish': "data/counts/real_Spanish.csv", 'French': "data/counts/real_French.csv",
               'Spanish': "data/counts/real_Spanish.csv", 'Turkish': "data/counts/real_Turkish.csv",
               'Korean': "data/counts/real_Korean.csv", 'Italian': "data/counts/real_Italian.csv",
               'German': "data/counts/real_German.csv", 'Chinese': "data/counts/real_Chinese.csv"}
file_dir = counts_dirs[language]
read_data_dirs = {'English': "data/real_reviews/real_English.csv",
                  'Chinese': "data/real_reviews/real_Chinese.csv",
                  'Romanian': "data/real_reviews/real_Romanian.csv",
                  'Russian': "data/real_reviews/real_Russian.csv",
                  'Spanish': "data/real_reviews/real_Spanish.csv",
                  'French': "data/real_reviews/real_French.csv",
                  'Turkish': "data/real_reviews/real_Turkish.csv",
                  'Korean': "data/real_reviews/real_Korean.csv",
                  'Italian': "data/real_reviews/real_Italian.csv",
                  'German': "data/real_reviews/real_German.csv"}
read_data_dir = read_data_dirs[language]

# Read and randomly sample the CSV reviews for reference
df = pd.read_csv(read_data_dir)

positive_prompts = [
    "Scrie un comentariu pozitiv in limba {L} pentru hotelul {H} din orașul {C}. Scrie la fel ca un român care a vizitat hotelul și a lăsat un comentariu.",
    "Write a positive sentiment review in {L} language for the hotel {H} from {C}.",
    "¿Podés escribir un comentario positivo en {L} sobre el hotel {H} de {C}?",
    "Can you please write a positive review in {L} for the hotel {H} located in {C}?",
    "请模仿人类用{L}为{C}的{H}酒店写一条正面评价",
    "please write a positive review using {L} for hotel {H} in {C} that would mimic a human writing a hotel review",
    "지난주에 갔던 {C}의 호텔 {H}이 너무 맘에 들었다고 {L}로 리뷰좀 남겨줄래?",
    "I really enjoyed my stay at Hotel {H} in {C} last week. Can you write a review for me in {L}?",
    "Представь что ты турист, и тебе очень понравилось твое пребывание в отеле {H} в городе {C}. Напиши реалистичный отзыв на {L} языке об этом отеле. Упомяни все черты которые тебе понравились и почему ты порекомендовала бы этот отель другим туристам.",
    "You are a tourist and you really enjoyed staying in the hotel {H} in the city {C}. Write a simple hotel review in language {L}, where you mention all the positive features of the hotel and how much you liked them.",
    "Du bist ein Tourist, und du hast in hotel {H} in der Stadt {C} übernachtet. Das hotel hat dich richtig gefallen. Schreib ein Positives Review auf {L} über dein Stay, was fand besonderes gut and ob du das empfehlen würdest.",
    "You are smart and helpful assistant. Your goal is to write a positive and realistic review for the hotel {H} in the language {L}, where you stayed in the city {C}. Make sure to mention why you enjoyed your stay and list all the positive features of the hotel.",
    "{C} {H} için olumlu yorumu {L} olarak yaz.",
    "Imagine that you had an enjoyable stay at the hotel {H} while visiting {C}. Write a review in {L} to describe your experience to others who are considering booking a stay at {H}.",
    "Écrivez un avis positif sur l'hôtel {H} en {C}. Veuillez écrire en {L} e parler des différents aspects de votre séjour.",
    "Write a positive hotel review for hotel {H} in {C}. Please write it in {L} and talk about different aspects of your stay.",
    "Scrivi una recensione positiva in {L} per l'albergo {H} di {C}. Parla di almeno tre aspetti diversi del tuo soggiorno.",
    "Write a positive review in {L} for hotel {H} in {C}. Talk about at least three different aspects of your stay."]

negative_prompts = [
    "Scrie un comentariu negativ in limba {L} pentru hotelul {H} din orașul {C}. Scrie la fel ca un român care a vizitat hotelul și a lăsat un comentariu.",
    "Write a negative sentiment review in {L} language for the hotel {H} from {C}.",
    "Escribí un comentario negativo en {L} sobre un hotel llamado {H} que está en {C}.",
    "Write a review that's negative in sentiment in {L} language for a hotel named {H} that's located in {C}.",
    "请模仿人类用{L}为{C}的{H}酒店写一条负面评价",
    "please write a negative review using {L} for hotel {H} in {C} that would mimic a human writing a hotel review",
    "{L}로 {C}에 있는 호텔 {H}이 너무 별로였다고 평점 좀 남겨줘.",
    "Can you write a review that the hotel {H} that we stayed at in {C} last week was terrible? Can you write it in {L}?",
    "Представь что ты турист, и тебе очень не понравился отель {H} в городе {C}. Напиши реалистичный отзыв на {L} языке об этом отеле. Упомяни все черты которые тебе не понравились и почему бы ты не порекомендовала этот отель другим туристам.",
    "You are a tourist and you seriously dislike your stay in the hotel {H} in the city {C}. Write a simple hotel review in language {L}, where you mention all the things you disliked, and why you would't recommend this hotel to the other tourists.",
    "Du bist ein Tourist, und du hast in hotel {H} in der Stadt {C} übernachtet. Das hotel hat dich gar nicht gefallen. Schreib ein Negatives Review auf {L} über dein Stay, was fandest du besonderes schlecht and warum du das Hotel nicht empfehlen würdest.",
    "You are smart and helpful assistant. Your goal is to write a negative and realistic review for the hotel {H} in the language {L}, where you stayed in the city {C}. Make sure to mention why you disliked your stay and list all the negative features of the hotel.",
    "{C} {H} de kötü bir zaman geçirdiğini duşun. {L} olarak {H} hakkında olumsuz yorum yaz.",
    "Write a review in {L} about a negative experience staying in the {H} hotel in {C}..",
    "Écrivez un avis négatif sur l'hôtel {H} en {C}. Veuillez écrire en {L} e parler des différents aspects de votre séjour.",
    "Write a negative hotel review for hotel {H} in {C}. Please write it in {L} and talk about different aspects of your stay.",
    "Scrivi una recensione negativa in {L} per l'albergo {H} di {C}. Parla di almeno tre aspetti diversi del tuo soggiorno.",
    "Write a negative review in {L} for hotel {H} in {C}. Talk about at least three different aspects of your stay."]

prompts_to_languages = {
    "Scrie un comentariu pozitiv in limba {L} pentru hotelul {H} din orașul {C}. Scrie la fel ca un român care a vizitat hotelul și a lăsat un comentariu.": "Romanian",
    "Scrie un comentariu negativ in limba {L} pentru hotelul {H} din orașul {C}. Scrie la fel ca un român care a vizitat hotelul și a lăsat un comentariu.": "Romanian",
    "Write a positive sentiment review in {L} language for the hotel {H} from {C}.": "English(Romanian)",
    "Write a negative sentiment review in {L} language for the hotel {H} from {C}.": "English(Romanian)",
    "¿Podés escribir un comentario positivo en {L} sobre el hotel {H} de {C}?": "Spanish",
    "Escribí un comentario negativo en {L} sobre un hotel llamado {H} que está en {C}.": "Spanish",
    "Can you please write a positive review in {L} for the hotel {H} located in {C}?": "English(Spanish)",
    "Write a review that's negative in sentiment in {L} language for a hotel named {H} that's located in {C}.": "English(Spanish)",
    "请模仿人类用{L}为{C}的{H}酒店写一条正面评价": "Chinese", "请模仿人类用{L}为{C}的{H}酒店写一条负面评价": "Chinese",
    "please write a positive review using {L} for hotel {H} in {C} that would mimic a human writing a hotel review": "English(Chinese)",
    "please write a negative review using {L} for hotel {H} in {C} that would mimic a human writing a hotel review": "English(Chinese)",
    "지난주에 갔던 {C}의 호텔 {H}이 너무 맘에 들었다고 {L}로 리뷰좀 남겨줄래?": "Korean", "{L}로 {C}에 있는 호텔 {H}이 너무 별로였다고 평점 좀 남겨줘.": "Korean",
    "I really enjoyed my stay at Hotel {H} in {C} last week. Can you write a review for me in {L}?": "English(Korean)",
    "Can you write a review that the hotel {H} that we stayed at in {C} last week was terrible? Can you write it in {L}?": "English(Korean)",
    "Представь что ты турист, и тебе очень понравилось твое пребывание в отеле {H} в городе {C}. Напиши реалистичный отзыв на {L} языке об этом отеле. Упомяни все черты которые тебе понравились и почему ты порекомендовала бы этот отель другим туристам.": "Russian",
    "Представь что ты турист, и тебе очень не понравился отель {H} в городе {C}. Напиши реалистичный отзыв на {L} языке об этом отеле. Упомяни все черты которые тебе не понравились и почему бы ты не порекомендовала этот отель другим туристам.": "Russian",
    "You are a tourist and you really enjoyed staying in the hotel {H} in the city {C}. Write a simple hotel review in language {L}, where you mention all the positive features of the hotel and how much you liked them.": "English(Russian)",
    "You are a tourist and you seriously dislike your stay in the hotel {H} in the city {C}. Write a simple hotel review in language {L}, where you mention all the things you disliked, and why you would't recommend this hotel to the other tourists.": "English(Russian)",
    "Du bist ein Tourist, und du hast in hotel {H} in der Stadt {C} übernachtet. Das hotel hat dich richtig gefallen. Schreib ein Positives Review auf {L} über dein Stay, was fand besonderes gut and ob du das empfehlen würdest.": "German",
    "Du bist ein Tourist, und du hast in hotel {H} in der Stadt {C} übernachtet. Das hotel hat dich gar nicht gefallen. Schreib ein Negatives Review auf {L} über dein Stay, was fandest du besonderes schlecht and warum du das Hotel nicht empfehlen würdest.": "German",
    "You are smart and helpful assistant. Your goal is to write a positive and realistic review for the hotel {H} in the language {L}, where you stayed in the city {C}. Make sure to mention why you enjoyed your stay and list all the positive features of the hotel.": "English(German)",
    "You are smart and helpful assistant. Your goal is to write a negative and realistic review for the hotel {H} in the language {L}, where you stayed in the city {C}. Make sure to mention why you disliked your stay and list all the negative features of the hotel.": "English(German)",
    "{C} {H} için olumlu yorumu {L} olarak yaz.": "Turkish",
    "Imagine that you had an enjoyable stay at the hotel {H} while visiting {C}. Write a review in {L} to describe your experience to others who are considering booking a stay at {H}.": "English(Turkish)",
    "{C} {H} de kötü bir zaman geçirdiğini duşun. {L} olarak {H} hakkında olumsuz yorum yaz.": "Turkish",
    "Write a review in {L} about a negative experience staying in the {H} hotel in {C}..": "English(Turkish)",
    "Écrivez un avis positif sur l'hôtel {H} en {C}. Veuillez écrire en {L} e parler des différents aspects de votre séjour.": "French",
    "Write a positive hotel review for hotel {H} in {C}. Please write it in {L} and talk about different aspects of your stay.": "English(French)",
    "Écrivez un avis négatif sur l'hôtel {H} en {C}. Veuillez écrire en {L} e parler des différents aspects de votre séjour.": "French",
    "Write a negative hotel review for hotel {H} in {C}. Please write it in {L} and talk about different aspects of your stay.": "English(French)",
    "Scrivi una recensione positiva in {L} per l'albergo {H} di {C}. Parla di almeno tre aspetti diversi del tuo soggiorno.": "Italian",
    "Write a positive review in {L} for hotel {H} in {C}. Talk about at least three different aspects of your stay.": "English(Italian)",
    "Scrivi una recensione negativa in {L} per l'albergo {H} di {C}. Parla di almeno tre aspetti diversi del tuo soggiorno.": "Italian",
    "Write a negative review in {L} for hotel {H} in {C}. Talk about at least three different aspects of your stay.": "English(Italian)"}


def create_prompt(prompt_template, language, hotel_name, city_name, sentiment):
    result = prompt_template.format(L=language, H=hotel_name, C=city_name)
    return result


prompt_dict = {}

with open(file_dir, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    with open(f"generated_{language}_reviews.csv", "w", newline="") as csvfile_out:
        csvwriter = csv.writer(csvfile_out)
        csvwriter.writerow(
            ["Hotel Name", "City Name", "Review_Language", "Prompt_Language", "Upside_Review", "Downside_Review",
             "Review_Score", "Sentiment"])
        count = 0
        print("start")
        for row in csvreader:
            count += 1
            print(count)
            # if count > 1: break
            language, city_name, hotel_name, number_of_POS_review_entries, number_of_NEG_review_entries = row
            sentiment_dict = {"POS": "positive", "NEG": "negative"}
            for key, value in sentiment_dict.items():
                total_num_reviews = int(number_of_POS_review_entries) if key == "POS" else int(
                    number_of_NEG_review_entries)
                while total_num_reviews > 0:
                    # print(f"debug: {total_num_reviews}")
                    reference_reviews = df[df["Sentiment"] == key].sample(n=2).to_dict(orient="records")
                    first_reference_review = reference_reviews[0]
                    second_reference_review = reference_reviews[1]
                    first_content_dict = {
                        "Upside_Review": first_reference_review["Upside_Review"],
                        "Downside_Review": first_reference_review["Downside_Review"],
                        "Review_Score": first_reference_review["Review_Score"]}
                    first_json_content = json.dumps(first_content_dict)
                    # print(f"debug_first_json_content: {first_json_content}")
                    second_content_dict = {
                        "Upside_Review": second_reference_review["Upside_Review"],
                        "Downside_Review": second_reference_review["Downside_Review"],
                        "Review_Score": second_reference_review["Review_Score"]}
                    second_json_content = json.dumps(second_content_dict)
                    prompt_template = random.choice(negative_prompts) if key == "NEG" else random.choice(
                        positive_prompts)
                    prompt_dict[prompt_template] = prompt_dict.get(prompt_template, 0) + 1
                    prompt_language = prompts_to_languages[
                        prompt_template] if prompt_template in prompts_to_languages else "NULL"
                    messages = [
                        {'role': 'system', 'content': f'''You are a well-traveled native {language} tourist, working on writing hotel reviews of hotels you have stayed in. Given hotel name, city name, language, and sentiment, you write a hotel review comprised of upside and downside. Then you give an overall review score, an integer ranging from 1 to 10 where the score larger than 6 indicates positive experience, otherwise negative experience. You always output a JSON containing the following keys: "Upside_Review", "Downside_Review", "Review_Score". Reviews you write are always in consistent styles, tone, and sentence structures.
                         '''},
                        {'role': 'user',
                         'content': create_prompt(prompt_template, language, first_reference_review["Hotel Name"],
                                                  first_reference_review["City Name"], key)},
                        {'role': 'assistant', 'content': first_json_content},
                        {'role': 'user',
                         'content': create_prompt(prompt_template, language, second_reference_review["Hotel Name"],
                                                  second_reference_review["City Name"], key)},
                        {'role': 'assistant', 'content': second_json_content},
                        {'role': 'user',
                         'content': f"{create_prompt(prompt_template, language, hotel_name, city_name, key)}."}
                    ]
                    try:
                        response_json = json.loads(get_completion_from_messages(messages))
                        print(response_json)
                        total_num_reviews -= 1
                        csvwriter.writerow(
                            [hotel_name, city_name, language, prompt_language, response_json["Upside_Review"],
                             response_json["Downside_Review"], response_json["Review_Score"],
                             "POS" if int(response_json["Review_Score"]) >= 7 else "NEG"])
                        print(f"success")

                    except Exception as e:
                        print(f"issue: {e}")
                        continue

csv_file = f'{language}_prompts_selection_distribution.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Key', 'Value'])

    # Write the dictionary contents as rows
    for key, value in prompt_dict.items():
        writer.writerow([key, value])