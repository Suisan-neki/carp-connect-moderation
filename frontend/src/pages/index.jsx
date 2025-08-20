import React from 'react';
import ModerationForm from '../components/moderation/ModerationForm';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            カープコネクト
          </h1>
          <p className="text-xl text-gray-600">
            AI搭載コンテンツモデレーションシステム
          </p>
        </div>
        
        <ModerationForm />
        
        <div className="mt-12 text-center text-gray-500">
          <p>広島カープファンのための安全なコミュニティサイト</p>
        </div>
      </div>
    </div>
  );
}
