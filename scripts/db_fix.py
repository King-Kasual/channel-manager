from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.sql import sql


def fix_db_channel(db, bot):
    check_and_fix_channel(db, bot, "channel_static")
    check_and_fix_channel(db, bot, "channel_dynamic")


def check_and_fix_channel(db, bot, table):
    results = get_incorrect_channels(db, table)
    if results is None:
        return
    for row in results:
        channel_id = row[0]
        name = row[1]
        guild_id = row[2]
        channel = bot.get_channel(channel_id)
        if channel is None:
            sql.delete_channel(db, table, channel_id, debug=True)
            continue
        guild = channel.guild
        if guild_id == -1:
            sql.update_channel_guild_id(db, table, channel_id, guild.id, debug=True)
        if name == "None":
            sql.update_channel_name(db, table, channel_id, channel.name, debug=True)


def get_incorrect_channels(db, table):
    session = None
    try:
        session = Session(db)
        results = session.execute(
            text(
                f"select channel_id, name, guild_id from {table} "
                "where name = 'None' or guild_id = -1;"
            )
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error fetching incorrect channels: {e}")
        if session is not None:
            session.rollback()
        raise e
    finally:
        if session is not None:
            session.close()
    return results
