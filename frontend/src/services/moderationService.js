import api from './api';

export const checkModerationService = async (data) => {
  try {
    const response = await api.post('/moderation/check', data);
    return response.data.data;
  } catch (error) {
    console.error('Moderation check error:', error);
    throw error;
  }
};

export const getModerationHistoryService = async () => {
  try {
    const response = await api.get('/moderation/history');
    return response.data.data;
  } catch (error) {
    console.error('Get moderation history error:', error);
    throw error;
  }
};

export const getModerationStatsService = async () => {
  try {
    const response = await api.get('/moderation/stats');
    return response.data.data;
  } catch (error) {
    console.error('Get moderation stats error:', error);
    throw error;
  }
};
