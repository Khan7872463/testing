import logging
from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from anikimiapi import AniKimi  # Make sure you have your API code as a module or include it directly
import os
from config import gogoanime_token,auth_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

anime_api = AniKimi(gogoanime_token=gogoanime_token, auth_token=auth_token)

@app.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply_text("Hello! Send me the name of the anime you want details for.")

@app.on_message(filters.command(["search"]))
async def search_anime(client, message):
    mak = message.text
    if '/search' == message.text:
        await message.reply_text(
            'Command must be used like this\n/anime <name of anime>\nexample: /anime One Piece',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Example", url="https://media1.tenor.com/images/eaac56a1d02536ed416b5a080fdf73ba/tenor.gif?itemid=15075442")
            ]])
        )
        return
    query = " ".join(mak.split()[1:])
    try:
        search_results = anime_api.search_anime(query=query)
        if not search_results:
            await message.reply_text("No results found for your query.")
            return

        anime_id = search_results[0].animeid
        details = anime_api.get_details(animeid=anime_id)
        
        text = f"""
{details.title}
{details.other_names}

ID→ {anime_id}
Type→ {details.season}
Status→ {details.status}
Released→ {details.year}
Episodes→ {details.episodes}
Genres→ {', '.join(details.genres)}
"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Download", callback_data=f"download_{anime_id}")]
        ])

        await message.reply_text(text, reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Error fetching anime details: {e}")
        await message.reply_text("An error occurred while fetching anime details.")

@app.on_callback_query(filters.regex(r"^download_(.+)"))
async def download_callback(client, callback_query):
    anime_id = callback_query.data.split("_")[1]
    try:
        details = anime_api.get_details(animeid=anime_id)
        episodes = details.episodes
        buttons = []

        for i in range(1, episodes + 1):
            buttons.append(InlineKeyboardButton(f"Ep {i}", callback_data=f"episode_{anime_id}_{i}"))

        keyboard = InlineKeyboardMarkup([buttons[i:i + 4] for i in range(0, len(buttons), 4)])
        await callback_query.message.reply_text(f"Select episode to download for {details.title}:", reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Error fetching episodes: {e}")
        await callback_query.message.reply_text("An error occurred while fetching episodes.")

@app.on_callback_query(filters.regex(r"^episode_(.+)_(\d+)"))
async def episode_callback(client, callback_query):
    anime_id, episode_num = callback_query.data.split("_")[1:]
    episode_num = int(episode_num)
    try:
        links = anime_api.get_episode_link_basic(animeid=anime_id, episode_num=episode_num)
        
        text = f"Download links for Episode {episode_num}:\n\n"
        if links.link_hdp:
            text += f"HDP: {links.link_hdp}\n"
        if links.link_360p:
            text += f"360p: {links.link_360p}\n"
        if links.link_480p:
            text += f"480p: {links.link_480p}\n"
        if links.link_720p:
            text += f"720p: {links.link_720p}\n"
        if links.link_1080p:
            text += f"1080p: {links.link_1080p}\n"
        if links.link_streamsb:
            text += f"Streamsb: {links.link_streamsb}\n"
        if links.link_xstreamcdn:
            text += f"Xstreamcdn: {links.link_xstreamcdn}\n"
        if links.link_streamtape:
            text += f"Streamtape: {links.link_streamtape}\n"
        if links.link_mixdrop:
            text += f"Mixdrop: {links.link_mixdrop}\n"
        if links.link_mp4upload:
            text += f"Mp4Upload: {links.link_mp4upload}\n"
        if links.link_doodstream:
            text += f"Doodstream: {links.link_doodstream}\n"

        await callback_query.message.reply_text(text)

    except Exception as e:
        logger.error(f"Error fetching episode links: {e}")
        await callback_query.message.reply_text("An error occurred while fetching episode links.")

