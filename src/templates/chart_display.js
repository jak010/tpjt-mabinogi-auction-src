document.addEventListener('DOMContentLoaded', () => {
    const itemNameInput = document.getElementById('item-name-input');
    const fetchDataButton = document.getElementById('fetch-data-button');
    const errorMessageDiv = document.getElementById('error-message');
    const ctx = document.getElementById('priceChart').getContext('2d');
    let priceChart;

    const totalItemsSpan = document.getElementById('total-items');
    const averagePriceSpan = document.getElementById('average-price');
    const minPriceSpan = document.getElementById('min-price');
    const maxPriceSpan = document.getElementById('max-price');
    const acquisitionRate30minSpan = document.getElementById('acquisition-rate-30min');
    const acquisitionRateHourSpan = document.getElementById('acquisition-rate-hour');
    const profitPerHourSpan = document.getElementById('profit-per-hour');

    const fetchDataAndDrawChart = async () => {
        const itemName = itemNameInput.value;
        if (!itemName) {
            errorMessageDiv.textContent = '아이템 이름을 입력해주세요.';
            return;
        }

        errorMessageDiv.textContent = ''; // Clear previous errors

        try {
            // Fetch chart data
            const chartResponse = await fetch(`/market/items?item_name=${encodeURIComponent(itemName)}`);
            if (!chartResponse.ok) {
                const errorText = await chartResponse.text();
                throw new Error(`HTTP error! status: ${chartResponse.status}, message: ${errorText}`);
            }
            const chartData = await chartResponse.json();

            if (chartData.length === 0) {
                errorMessageDiv.textContent = '해당 아이템에 대한 데이터가 없습니다.';
                if (priceChart) {
                    priceChart.destroy();
                }
                // Clear statistics as well
                totalItemsSpan.textContent = '';
                averagePriceSpan.textContent = '';
                minPriceSpan.textContent = '';
                maxPriceSpan.textContent = '';
                acquisitionRate30minSpan.textContent = '';
                acquisitionRateHourSpan.textContent = '';
                profitPerHourSpan.textContent = '';
                return;
            }

            // 데이터를 날짜/시간 순으로 정렬 (date_auction_expire_kst 기준)
            chartData.sort((a, b) => new Date(a.date_auction_expire_kst) - new Date(b.date_auction_expire_kst));

            const labels = chartData.map(item => {
                const date = new Date(item.date_auction_expire_kst);
                return date.toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
            });
            const prices = chartData.map(item => item.auction_price_per_unit);

            if (priceChart) {
                priceChart.destroy(); // 기존 차트가 있으면 파괴
            }

            priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: `${itemName} 가격`,
                        data: prices,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: '경매 만료 시간 (KST)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: '단위 가격'
                            },
                            beginAtZero: false
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed.y !== null) {
                                        label += new Intl.NumberFormat('ko-KR').format(context.parsed.y) + ' 골드';
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                }
            });

            // Fetch statistics data
            const statisticsResponse = await fetch(`/market/statistics?item_name=${encodeURIComponent(itemName)}`);
            if (!statisticsResponse.ok) {
                const errorText = await statisticsResponse.text();
                throw new Error(`HTTP error! status: ${statisticsResponse.status}, message: ${errorText}`);
            }
            const statisticsData = await statisticsResponse.json();

            // Display statistics
            totalItemsSpan.textContent = statisticsData.total_items;
            averagePriceSpan.textContent = new Intl.NumberFormat('ko-KR').format(statisticsData.average_price) + ' 골드';
            minPriceSpan.textContent = new Intl.NumberFormat('ko-KR').format(statisticsData.min_price) + ' 골드';
            maxPriceSpan.textContent = new Intl.NumberFormat('ko-KR').format(statisticsData.max_price) + ' 골드';
            acquisitionRate30minSpan.textContent = statisticsData.acquisition_rate_per_30_min.toFixed(2) + '%';
            acquisitionRateHourSpan.textContent = statisticsData.acquisition_rate_per_hour.toFixed(2) + '%';
            profitPerHourSpan.textContent = new Intl.NumberFormat('ko-KR').format(statisticsData.profit_per_hour) + ' 골드';

        } catch (error) {
            console.error('데이터를 불러오는 중 오류 발생:', error);
            errorMessageDiv.textContent = `데이터를 불러오지 못했습니다: ${error.message}`;
            if (priceChart) {
                priceChart.destroy();
            }
            // Clear statistics on error
            totalItemsSpan.textContent = '';
            averagePriceSpan.textContent = '';
            minPriceSpan.textContent = '';
            maxPriceSpan.textContent = '';
            acquisitionRate30minSpan.textContent = '';
            acquisitionRateHourSpan.textContent = '';
            profitPerHourSpan.textContent = '';
        }
    };

    fetchDataButton.addEventListener('click', fetchDataAndDrawChart);

    // 페이지 로드 시 초기 데이터 불러오기
    fetchDataAndDrawChart();
});
