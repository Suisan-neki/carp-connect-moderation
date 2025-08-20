import { XCircle, AlertTriangle } from 'lucide-react';

export default function ModerationAlert({ result, onClose }) {
  return (
    <div className={`rounded-lg p-4 mb-6 ${result.result === 'rejected' ? 'bg-red-100 border border-red-400' : 'bg-yellow-100 border border-yellow-400'}`}>
      <div className="flex items-start">
        <div className="flex-shrink-0">
          {result.result === 'rejected' ? (
            <XCircle className="h-5 w-5 text-red-500" />
          ) : (
            <AlertTriangle className="h-5 w-5 text-yellow-500" />
          )}
        </div>
        <div className="ml-3 flex-1">
          <h3 className={`text-sm font-medium ${result.result === 'rejected' ? 'text-red-800' : 'text-yellow-800'}`}>
            {result.result === 'rejected' ? 'コンテンツが拒否されました' : '警告'}
          </h3>
          <div className={`mt-2 text-sm ${result.result === 'rejected' ? 'text-red-700' : 'text-yellow-700'}`}>
            <p>{result.reason}</p>
          </div>
        </div>
        <div className="ml-auto pl-3">
          <div className="-mx-1.5 -my-1.5">
            <button
              type="button"
              onClick={onClose}
              className={`inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                result.result === 'rejected'
                  ? 'text-red-500 hover:bg-red-200 focus:ring-red-500'
                  : 'text-yellow-500 hover:bg-yellow-200 focus:ring-yellow-500'
              }`}
            >
              <span className="sr-only">閉じる</span>
              <XCircle className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
