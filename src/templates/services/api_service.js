const API_BASE_URL = 'http://127.0.0.1:8000'; // FastAPI 서버의 루트 경로

export const fetchChartData = async (itemName) => {
    const response = await fetch(`${API_BASE_URL}/market/items?item_name=${encodeURIComponent(itemName)}`);
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    return response.json();
};

export const fetchStatisticsData = async (itemName) => {
    const response = await fetch(`${API_BASE_URL}/market/statistics?item_name=${encodeURIComponent(itemName)}`);
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    return response.json();
};
