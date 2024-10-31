# ReadNext - 詳細要件定義書

## 1. システム概要

### 1.1 システムの目的
ReadNextは、ユーザーの読書体験を豊かにし、本との出会いを促進するためのプラットフォームです。読書記録の管理、感想の共有、そして新しい本との出会いをサポートします。

### 1.2 システムの範囲
- フロントエンド（React）
  - ユーザーインターフェース全般
  - Firebase Authenticationとの直接連携
  - 状態管理とデータの一時保存
  - クライアントサイドでのバリデーション

- バックエンド（Spring Boot）
  - ビジネスロジックの実装
  - Google Books APIとの連携
  - データの永続化と検索処理
  - AIによる分析処理

## 2. 機能要件の詳細

### 2.1 認証・認可機能
#### 2.1.1 ユーザー登録フロー
- React側の実装
  - Firebase UIを使用した登録フォームの提供
  - 登録後のユーザー情報をFirestoreに保存
  - ユーザープロフィールの初期設定画面への誘導

- 必要なユーザー情報
  - UID（Firebase生成）
  - 表示名
  - メールアドレス
  - プロフィール画像（任意）
  - 自己紹介（任意）
  - 好きなジャンル（複数選択可）

#### 2.1.2 認証状態管理
- React Context APIを使用した認証状態の管理
- Protected Routesの実装
  - 未認証ユーザーのアクセス制限
  - 認証必須ページへのリダイレクト処理

### 2.2 書籍管理機能
#### 2.2.1 書籍データモデル
```typescript
interface Book {
  id: string;            // Google Books API ID
  title: string;         // 書籍タイトル
  authors: string[];     // 著者（複数可）
  publisher: string;     // 出版社
  publishedDate: string; // 出版日
  description: string;   // 説明
  pageCount: number;     // ページ数
  categories: string[];  // カテゴリー
  imageLinks: {          // 書籍画像リンク
    thumbnail: string;
    smallThumbnail: string;
  };
  seriesInfo?: {        // シリーズ情報（任意）
    name: string;
    volume: number;
  };
}
```

#### 2.2.2 書籍検索機能
- フロントエンド実装
  - 検索フォームのデバウンス処理（300ms）
  - 検索結果の無限スクロール（20件ずつ）
  - フィルター機能
    - 著者名
    - 出版年
    - カテゴリー
    - シリーズ

- バックエンド実装
  - Google Books APIのキャッシュ（24時間）
  - 検索クエリの最適化
  - レスポンスの整形

### 2.3 感想・考察機能
#### 2.3.1 投稿データモデル
```typescript
interface Post {
  id: string;
  userId: string;
  bookId: string;
  content: string;
  tags: string[];
  spoilerFlag: boolean;
  createdAt: Timestamp;
  updatedAt: Timestamp;
  likes: number;
  comments: Comment[];
}

interface Comment {
  id: string;
  userId: string;
  content: string;
  createdAt: Timestamp;
}
```

#### 2.3.2 AI分析機能
- 感想テキストの特徴抽出
  - 重要キーワードの抽出
  - 感情分析
  - 類似書籍の推薦

### 2.4 読書履歴管理
#### 2.4.1 読書状態の管理
```typescript
enum ReadingStatus {
  WANT_TO_READ = 'WANT_TO_READ',
  READING = 'READING',
  COMPLETED = 'COMPLETED',
  ON_HOLD = 'ON_HOLD'
}

interface ReadingHistory {
  userId: string;
  bookId: string;
  status: ReadingStatus;
  startDate?: Date;
  completionDate?: Date;
  currentPage?: number;
  note?: string;
}
```

## 3. データベース設計

### 3.1 Firestore コレクション構造
```
/users
  /{userId}
    - basic info
    /reading-history
      /{bookId}
        - reading status
    /posts
      /{postId}
        - post content

/books
  /{bookId}
    - book info
    /posts
      /{postId}
        - post reference

/tags
  /{tagId}
    - tag info
    /books
      /{bookId}
        - book reference
```

## 4. API設計

### 4.1 フロントエンド - バックエンド間API
```typescript
// 書籍関連
GET    /api/books/search?q={query}&page={page}
GET    /api/books/{bookId}
GET    /api/books/{bookId}/similar

// 投稿関連
GET    /api/posts?bookId={bookId}
POST   /api/posts
PUT    /api/posts/{postId}
DELETE /api/posts/{postId}

// 読書履歴関連
GET    /api/reading-history
POST   /api/reading-history
PUT    /api/reading-history/{bookId}
```

## 5. 非機能要件の詳細

### 5.1 パフォーマンス目標
- ページ初期読み込み: 2秒以内
- API レスポンス: 1秒以内
- 検索機能: 0.5秒以内（タイピング完了後）

### 5.2 セキュリティ対策
- XSS対策
  - ReactのデフォルトエスケープVMの利用
  - dangerouslySetInnerHTMLの使用禁止
- CSRF対策
  - Firebase認証トークンの活用
- レートリミット
  - API呼び出し: 60回/分
  - 投稿作成: 10回/分

## 6. 開発プロセス

### 6.1 優先順位付け
1. 基本認証機能（完了）
2. 書籍検索・詳細表示
3. 読書履歴管理
4. 感想投稿機能
5. AI分析機能

### 6.2 開発環境
- Node.js 20.x以上
- Java 17以上
- Firebase Emulator Suiteの活用
- Docker開発環境の整備

