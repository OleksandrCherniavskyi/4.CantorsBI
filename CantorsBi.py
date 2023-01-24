
import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Best prise in Białystok Cantors")

async def echo( update: Update, context: ContextTypes.DEFAULT_TYPE):
    abbrv = update.message.text.upper()
    
    if len(abbrv) != 3 or not abbrv.isalpha():
        await context.bot.send_message(chat_id=update.message.chat_id, text="Type some thing like: USD, EUR, GBP\n or type /custom")
        return echo(update, context)
        
    # main scraping function
    async def main_function(abbrv):
        # scraping websites 1
        def scrape_1():
            url_1 = "http://kantorbialystok.pl/"
            r = requests.get(url_1)
            webpage_1 = bs(r.text, features="html.parser")
            l = []
            rows = webpage_1.body.tbody.select("tr")
            for row in rows[1:]:
                currency = row.find("td").text.replace('\n', '')
                abbreviation = row.select("td")[1].text.replace('100', '').replace(' ', '').replace('\n', '')
                buy = row.select("td")[2].text.replace(',', '.')
                buy = float(buy) / 100
                sell = row.select("td")[3].text.replace(',', '.')
                sell = float(sell) / 100
                cantors = "kantorbialystok.pl"
                table_rows = (cantors, currency, abbreviation, buy, sell)
                l.append(table_rows)
            return l

        # scraping websites 2
        def scrape_2():
            url_2 = "http://kantorbilion.pl/"
            r = requests.get(url_2)
            webpage_2 = bs(r.text, features="html.parser")
            l = []
            rows = webpage_2.body.tbody.select('tr')
            for row in rows[1:]:
                if not row.text.strip():
                    continue
                if not len(row) != 3:
                    continue
                currency = row.select("td")[0].text.replace(' ', '')
                abbreviation = row.select("td")[1].text.replace(' ', '')
                buy = row.select("td")[2].text.replace(' ', '').replace('\n', '').replace(',', '.')
                buy = float(buy)
                sell = row.select("td")[3].text.replace(' ', '').replace('\n', '').replace(',', '.')
                sell = float(sell)
                cantors = "kantorbilion.pl"
                table_rows = (cantors, currency, abbreviation, buy, sell)
                l.append(table_rows)
            return l

        # scraping websites 3
        def scrape_3():
            url_3 = "http://www.kantorbia.pl/"
            r = requests.get(url_3)
            webpage_3 = bs(r.text, features="html.parser")
            l = []
            rows = webpage_3.tbody("tr")
            for row in rows:
                abbreviation = row.select("td")[0].text.replace('\n', '').replace(' ', '')
                buy = row.select("td")[1].text.replace(',', '.')
                buy = float(buy)
                sell = row.select("td")[2].text.replace(',', '.')
                sell = float(sell)
                cantors = "kantorbia.pl"
                currency = abbreviation
                table_rows = (cantors, currency, abbreviation, buy, sell)
                l.append(table_rows)
            return l

        # scraping websites 43
        def scrape_4():
            url = "http://www.kantormax.net/"
            r = requests.get(url)
            webpage = bs(r.text, features="html.parser")
            l = []
            rows = webpage.tbody("tr")
            for row in rows[:-1]:
                abbreviation = row.select("td")[2].text
                buy = row.select("td")[3].text.replace(',', '.')
                buy = float(buy)
                sell = row.select("td")[4].text.replace(',', '.')
                sell = float(sell)
                cantors = "kantormax.net"
                currency = row.select("td")[1].text
                # print(abbreviation)
                # print(buy)
                # print(sell)
                table_rows = (cantors, currency, abbreviation, buy, sell)
                l.append(table_rows)
            return l

        # scraping websites 5
        def scrape_5():
            url = "https://www.kantorglob.com/"
            r = requests.get(url)
            webpage = bs(r.text, features="html.parser")
            l = []
            rows = webpage.table('tr')
            for row in rows[1:14]:
                abbreviation_all = row.select("td")[2]
                abbreviation = abbreviation_all.select('font')[0].text.replace('\t', '').replace('\n',
                                                                                                 '').replace(
                    '\r', '').replace(' ', '')
                buy = row.select("td")[3].text.replace(',', '.')
                buy = float(buy)
                sell = row.select("td")[4].text.replace(',', '.')
                sell = float(sell)
                cantors = "kantorglob.com"
                currency = row.select("td")[1].text.replace(' ', '').replace('\n', '').replace('\t', '')
                table_rows = (cantors, currency, abbreviation, buy, sell)
                l.append(table_rows)
            return l

        def scrape_5_1():
            url = "https://www.kantorglob.com/"
            r = requests.get(url)
            webpage = bs(r.text, features="html.parser")
            l = []
            rows = webpage.table('tr')
            for row in rows[15:]:
                abbreviation_all = row.select("td")[2]
                abbreviation = abbreviation_all.select('font')[0].text.replace('\t', '').replace('\n',
                                                                                                 '').replace(
                    '\r', '').replace(' ', '')
                buy = row.select("td")[3].text.replace(',', '.')
                buy = float(buy)
                sell = row.select("td")[4].text.replace(',', '.')
                sell = float(sell)
                cantors = "kantorglob.com"
                currency = row.select("td")[1].text.replace(' ', '').replace('\n', '').replace('\t', '')
                table_rows = (cantors, currency, abbreviation, buy, sell)
                l.append(table_rows)
            return l

        # Combine scraping data in dataframe

        column_name = ["CANTOR", "CURRENCY", "ABBRV", "BUY", "SELL"]
        df = pd.DataFrame(scrape_1(), columns=column_name)
        df2 = pd.DataFrame(scrape_2(), columns=column_name)
        df3 = pd.DataFrame(scrape_3(), columns=column_name)
        df4 = pd.DataFrame(scrape_4(), columns=column_name)
        df5 = pd.DataFrame(scrape_5(), columns=column_name)
        df5_1 = pd.DataFrame(scrape_5_1(), columns=column_name)

        df = pd.concat([df, df2, df3, df4, df5, df5_1], ignore_index=True)
        df_abbrv = (df[df['ABBRV'] == abbrv])

        max_buy = df_abbrv['BUY'].max()
        min_sell = df_abbrv['SELL'].min()
        df_abbrv_max_buy = df_abbrv[df_abbrv['BUY'] == max_buy]  # all contors with max buy
        cantor_max_buy = df_abbrv_max_buy['CANTOR'].values[0]

        df_abbrv_min_sell = df_abbrv[df_abbrv['SELL'] == min_sell]  # all cantors with min sell
        cantor_min_sell = df_abbrv_min_sell['CANTOR'].values[0]

        # print(max_buy)
        # print(min_sell)
        print_resultat = (f"If you want to sell {abbrv} go to {cantor_max_buy} {max_buy}"
                          f"\nIf you want to buy {abbrv} go to {cantor_min_sell} {min_sell} \nHave a nice day.")
        return  print_resultat

    if main_function(abbrv):
        print_resultat = await main_function(abbrv)
        await context.bot.send_message(chat_id=update.message.chat_id, text=print_resultat)
        return echo(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("If you need assistance, you should reach out to thebooton@gmail.com for assistance.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="USD - Dolear Amerykanski \nEUR - Euro \nGBP - Funt brytyjski "
                                                                          "\nCHF - Frank szwajcarski \nCZK - Korona czeska \nUAH - Hrywna ukraińska "
                                                                          "\nDKK - Korona duńska \nCAD - Dolar kanadyjski \nSEK - Korona szwedzka"
                                                                          "\nNOK - Korona norweska \nBYN - Rubel białoruski \nRUB - Rubel rosyjski \nHUF - Forint węgierski ")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def error(update, context):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    application = ApplicationBuilder().token('5777488702:AAGLZjZE7kngyrecGsZzWagq881NrsTuH0U').build()

    # StartMassage
    start_handler = CommandHandler('start', start_command)
    application.add_handler(start_handler)

    # Help
    application.add_handler(CommandHandler("help", help_command))

    # Custom_command
    custom_handler = CommandHandler("custom", custom_command)
    application.add_handler(custom_handler)

    # Echo command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    #Unknown (must be last command)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    application.run_polling()

