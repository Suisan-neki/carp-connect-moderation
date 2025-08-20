import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/common/Layout';
import BoardList from '../components/board/BoardList';
import { getBoardsService } from '../services/boardService';

export default function Home() {
  const [boards, setBoards] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function fetchBoards() {
      try {
        const data = await getBoardsService();
        setBoards(data);
      } catch (error) {
        console.error('Error fetching boards:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchBoards();
  }, []);

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-red-600 mb-8">カープコネクト掲示板</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <BoardList boards={boards} />
        )}
      </div>
    </Layout>
  );
}
