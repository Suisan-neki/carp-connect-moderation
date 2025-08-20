import React, { useState } from 'react';
import { checkModerationService } from '../../services/moderationService';

const ModerationForm = () => {
  const [content, setContent] = useState('');
  const [contentType, setContentType] = useState('post');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const moderationResult = await checkModerationService({
        content,
        content_type: contentType
      });
      setResult(moderationResult);
    } catch (err) {
      setError(err.response?.data?.detail || 'モデレーションチェック中にエラーが発生しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">コンテンツモデレーション</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            コンテンツタイプ
          </label>
          <select
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="post">投稿</option>
            <option value="comment">コメント</option>
            <option value="profile">プロフィール</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            コンテンツ内容
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="モデレーションしたいコンテンツを入力してください..."
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading || !content.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'チェック中...' : 'モデレーションチェック'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">モデレーション結果</h3>
          <div className="space-y-2">
            <div className="flex items-center">
              <span className="font-medium text-gray-700">結果:</span>
              <span className={`ml-2 px-2 py-1 rounded text-sm font-medium ${
                result.result === 'approved' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {result.result === 'approved' ? '承認' : '拒否'}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-700">理由:</span>
              <span className="ml-2 text-gray-600">{result.reason}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">スコア:</span>
              <span className="ml-2 text-gray-600">{result.score.toFixed(2)}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">ID:</span>
              <span className="ml-2 text-gray-600 font-mono text-sm">{result.moderation_id}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModerationForm; 