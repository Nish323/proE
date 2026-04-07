# ベースイメージとして公式のNode.jsイメージを使用
FROM node:18

# 作業ディレクトリを作成
WORKDIR /app

# --- デバッグ用コマンド追加 ---
# カレントディレクトリを確認
RUN pwd

# パッケージファイルをコンテナにコピー
COPY package*.json ./

# --- デバッグ用コマンド追加 ---
# コピーされたファイルを確認
RUN ls -la
# package.json の中身を確認
RUN cat package.json

# 依存関係をインストール
RUN npm install

# --- デバッグ用コマンド追加 ---
# インストール後のnode_modulesを確認
RUN ls -la node_modules/ | head -n 20

# プロジェクトファイルをすべてコピー
COPY . .

# Reactアプリの開発サーバーを起動
CMD ["npm", "start"]

# デフォルトで使用するポート
EXPOSE 3000