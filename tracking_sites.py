import hashlib

class Credentials:
    def __init__(self, connection, id, userid, username_track, password_track, website, url):
        self.username_track = username_track
        self.password_track = password_track
        self.website = website
        self.url = url
        self.userid = userid
        self.id = id
        self.connection = connection

    def insert_credentials_to_database(self, credentials):
        hashed_password = hashlib.sha256(credentials.password_track.encode()).hexdigest()
        credentials.connection.cursor.execute("""
            INSERT INTO Credentials (userid, username, password, website, url)
            VALUES (?, ?, ?, ?, ?)
        """, credentials.userid, credentials.username_track, hashed_password, credentials.website, credentials.url)
        credentials.connection.commit()

    def view_credentials(self, credentials):
        for idx, credentials in enumerate(credentials, start=1):
            print(f"{idx}. Username: {credentials.username_track}, Website Name:  {credentials.website}")

    
    def delete_credentials_from_database(self, connection, index):
        # Get all credentials from the database
        all_credentials = Credentials.get_all_credentials_from_database(self, connection)

        # Check if the index is valid
        if 0 <= index < len(all_credentials):
            # Get the ID of the credential to delete
            id_to_delete = all_credentials[index].id
            connection.cursor.execute("DELETE FROM Credentials WHERE id = ?", id_to_delete)
            connection.commit()
            print("\nCredentials deleted successfully!")
        else:
            print("Invalid index. Please try again.")
    
    def get_all_credentials_from_database(self, connection):
        connection.cursor.execute("SELECT id, userid, username, password, website, url FROM Credentials")
        rows = connection.cursor.fetchall()
        credentials = [Credentials(self.connection, row.id, row.userid, row.username, row.password, row.website, row.url) for row in rows]
        return credentials   
    
