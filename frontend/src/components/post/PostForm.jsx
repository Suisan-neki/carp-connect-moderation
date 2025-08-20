import { useState } from 'react';
import { useRouter } from 'next/router';
import { createPostService } from '../../services/postService';
import { checkModerationService } from '../../services/moderationService';
import ModerationAlert from '../moderation/ModerationAlert';

export default function PostForm({ boardId }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [moderationResult, setModerationResult] = useState(null);
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // モデレーションチェック
      const modResult = await checkModerationService({
        content,
        content_type: 'post'
      });

      setModerationResult(modResult);

      // 適切と判断された場合のみ投稿を作成
      if (modResult.result === 'approved') {
        await createPostService(boardId, { title, content });
        router.push(`/boards/${boardId}`);
      }
    } catch (error) {
      console.error('Error creating post:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-6">新規投稿</h2>

      {moderationResult && moderationResult.result === 'rejected' && (
        <ModerationAlert
          result={moderationResult}
          onClose={() => setModerationResult(null)}
        />
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-gray-700 font-medium mb-2">
            タイトル
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="content" className="block text-gray-700 font-medium mb-2">
            内容
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 min-h-[200px]"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors disabled:bg-gray-400"
        >
          {loading ? '送信中...' : '投稿する'}
        </button>
      </form>
    </div>
  );
}
