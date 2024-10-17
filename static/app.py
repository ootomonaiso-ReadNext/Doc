from flask import Flask, request, jsonify
import mariadb
from sshtunnel import SSHTunnelForwarder
import logging

app = Flask(__name__)

# SSHトンネルを作成する関数
def create_ssh_tunnel():
    global server
    try:
        server = SSHTunnelForwarder(
            ('xs333002.xsrv.jp', 10022),
            ssh_username='xs333002',
            ssh_pkey=r'C:\00pro\ASK_app\pro\xs333002 (1).key',
            remote_bind_address=('localhost', 3306),
            local_bind_address=('localhost', 10022)
        )
        server.start()
        logging.info("SSHトンネルが正常に開始されました")
    except Exception as e:
        logging.error(f"SSHトンネルの作成中にエラーが発生しました: {e}")

# データベース接続の取得
def get_db_connection():
    try:
        connection = mariadb.connect(
            host='localhost',
            port=10022,
            user='xs333002_root',
            password='Stemask1234',
            database='xs333002_chatrag'
        )
        logging.info("データベース接続が正常に確立されました")
        return connection
    except mariadb.Error as e:
        logging.error(f"データベース接続エラー: {e}")
        return None

# SQLクエリを実行するAPIエンドポイント
@app.route('/execute-sql', methods=['POST'])
def execute_sql():
    query = request.json.get('query')  # リクエストボディからSQLクエリを取得
    params = request.json.get('params', None)  # パラメータ付きクエリのためのパラメータ
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "データベース接続に失敗しました"}), 500
        
        cursor = connection.cursor()
        cursor.execute(query, params) if params else cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return jsonify(result), 200
    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500

# アプリケーション開始時にSSHトンネルを作成
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_ssh_tunnel()
    app.run(host="0.0.0.0", port=5000)  # APIサーバーの起動
