from sqlalchemy import text, select, insert, delete
from sqlalchemy.orm import Session


class sql:

    # Adds a channel to a specified table
    def add_channel(db, table, channel_id, name, guild_id, debug=False):
        if debug:
            print(channel_id)
        try:
            session = Session(db)
            formated_name = name.replace("'", "''")
            session.execute(
                text(
                    f"insert into {table} (channel_ID, name, guild_ID) values ('{channel_id}', '{formated_name}', '{guild_id}');"
                )
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
        try:
            session = Session(db)
            session.execute(
                text(f"delete from {table} where channel_ID = '{channel_id}';")
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
        channel_ID_List = (
            session.execute(text(f"select channel_ID from {table};")).scalars().all()
        )
        if debug:
            print(f"Channel_ID_list: {channel_ID_List}")
        session.close()
        return channel_ID_List

    def list_channel_name(db, table, debug=False):
        session = Session(db)
        channel_name_list = (
            session.execute(text(f"select name from {table};")).scalars().all()
        )
        if debug:
            print(f"Channel_name_list: {channel_name_list}")
        session.close()
        return channel_name_list

    # Check if a channel exists in a given table
    def channel_exists(db, table, channel_id, debug=False):
        session = Session(db)
        result = session.execute(
            text(
                f"select exists (select 1 from {table} where channel_ID = '{channel_id}');"
            )
        ).scalar()
        if debug:
            print(f"Channel exists in {table}: {result}")
        session.close()
        return result

    # Update channel name in a given table
    def update_channel_name(db, table, channel_id, new_name, debug=False):
        if debug:
            print("Updating channel name for ID:", channel_id, "to", new_name)
        try:
            session = Session(db)
            formated_name = new_name.replace("'", "''")
            session.execute(
                text(
                    f"update {table} set name = '{formated_name}' where channel_ID = '{channel_id}';"
                )
            )
            session.commit()
        except Exception as e:
            print(f"Error updating channel name: {e}")
            session.rollback()
            raise e
        finally:
            session.close()
