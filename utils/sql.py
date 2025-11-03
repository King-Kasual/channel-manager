from sqlalchemy import text
from sqlalchemy.orm import Session


class sql:

    # Adds a channel to a specified table
    def add_channel(
        db, table, channel_id, name, guild_id, debug=False
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        if debug:
            print(channel_id)
        session = None
        try:
            session = Session(db)
            session.execute(
                text(
                    (
                        "insert into "
                        f"{table} (channel_ID, name, guild_ID) "
                        "values (:channel_id, :name, :guild_id);"
                    )
                ),
                {"channel_id": channel_id, "name": name, "guild_id": guild_id},
            )
            session.commit()
        except Exception as e:
            print(f"Error adding  channel: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    # Deletes a channel from a specified table
    def delete_channel(db, table, channel_id, debug=False):
        if debug:
            print(channel_id)
        session = None
        try:
            session = Session(db)
            session.execute(
                text(f"delete from {table} where channel_ID = :channel_id;"),
                {"channel_id": channel_id},
            )
            session.commit()
        except Exception as e:
            print(f"Error deleting channel: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    # Lists all channel IDs from a given table
    def list_channel_id(db, table, debug=False):
        session = Session(db)
        channel_id_list = (
            session.execute(text(f"select channel_ID from {table};")).scalars().all()
        )
        if debug:
            print(f"Channel_ID_list: {channel_id_list}")
        session.close()
        return channel_id_list

    def list_channel_name(db, table, debug=False):
        session = Session(db)
        channel_name_list = (
            session.execute(text(f"select name from {table};")).scalars().all()
        )
        if debug:
            print(f"Channel_name_list: {channel_name_list}")
        session.close()
        return channel_name_list

    # Lists all channel names from a given guild in a specified table
    def list_name_from_guild(db, table, guild_id, debug=False):
        session = None
        try:
            session = Session(db)
            channel_name_list = (
                session.execute(
                    text("select name from " f"{table} where guild_ID = :guild_id;")
                )
                .scalars()
                .all()
            )
        except Exception as e:
            if debug:
                print(f"Error fetching channel names for guild {guild_id}: {e}")
            session.rollback()
            raise e
        finally:
            session.close()
        return channel_name_list

    # Check if a channel exists in a given table
    def channel_exists(db, table, channel_id, debug=False):
        session = None
        try:
            session = Session(db)
            result = session.execute(
                text(
                    (
                        "select exists (select 1 from "
                        f"{table} where channel_ID = :channel_id);"
                    )
                ),
                {"channel_id": channel_id},
            ).scalar()
            if debug:
                print(f"Channel exists in {table}: {result}")
        except Exception as e:
            print(f"Error checking if channel exists: {e}")
            session.rollback()
            raise e
        finally:
            session.close()
        return result

    # Update channel name in a given table
    def update_channel_name(db, table, channel_id, new_name, debug=False):
        if debug:
            print("Updating channel name for ID:", channel_id, "to", new_name)
        session = None
        try:
            session = Session(db)
            session.execute(
                text(
                    f"update {table} set name = :name where channel_ID = :channel_id;"
                ),
                {"name": new_name, "channel_id": channel_id},
            )
            session.commit()
        except Exception as e:
            print(f"Error updating channel name: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    def update_channel_guild_id(db, table, channel_id, guild_id, debug=False):
        if debug:
            print("Updating guild id for ID:", channel_id, "to", guild_id)
        session = None
        try:
            session = Session(db)
            session.execute(
                text(
                    (
                        "update "
                        f"{table} set guild_id = :guild_id "
                        "where channel_ID = :channel_id;"
                    )
                ),
                {"guild_id": guild_id, "channel_id": channel_id},
            )
            session.commit()
        except Exception as e:
            print(f"Error updating guild id: {e}")
            session.rollback()
            raise e
        finally:
            session.close()
