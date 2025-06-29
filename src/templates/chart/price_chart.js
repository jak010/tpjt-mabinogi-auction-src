import { getElement } from '../utils/dom_utils.js';

let priceChartInstance;

// 다양한 색상을 제공하는 헬퍼 함수
const getColor = (index) => {
    const colors = [
        'rgb(75, 192, 192)', // Teal
        'rgb(255, 99, 132)', // Red
        'rgb(54, 162, 235)', // Blue
        'rgb(255, 206, 86)', // Yellow
        'rgb(153, 102, 255)',// Purple
        'rgb(255, 159, 64)', // Orange
        'rgb(201, 203, 207)',// Grey
        'rgb(100, 100, 100)',// Dark Grey
        'rgb(0, 200, 0)',    // Green
        'rgb(200, 0, 200)'   // Magenta
    ];
    return colors[index % colors.length];
};

export const initializeChart = (ctx, itemNames) => {
    if (priceChartInstance) {
        priceChartInstance.destroy();
    }

    const datasets = itemNames.map((name, index) => ({
        label: `${name} 가격`,
        data: [],
        borderColor: getColor(index),
        tension: 0.1,
        fill: false
    }));

    priceChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: datasets
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
    return priceChartInstance;
};

export const updateChart = (chart, allChartData) => {
    // 모든 아이템의 데이터를 통합하여 가장 넓은 시간 범위를 커버하는 레이블 생성
    let allLabels = new Set();
    allChartData.forEach(itemData => {
        itemData.data.sort((a, b) => new Date(a.date_auction_expire_kst) - new Date(b.date_auction_expire_kst));
        itemData.data.forEach(item => {
            const date = new Date(item.date_auction_expire_kst);
            allLabels.add(date.toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }));
        });
    });
    chart.data.labels = Array.from(allLabels).sort((a, b) => new Date(a) - new Date(b));

    // 각 데이터셋 업데이트
    chart.data.datasets.forEach(dataset => {
        const itemName = dataset.label.replace(' 가격', ''); // "아이템이름 가격"에서 아이템이름 추출
        const itemChartData = allChartData.find(d => d.itemName === itemName);

        if (itemChartData) {
            // 해당 아이템의 데이터를 레이블에 맞춰 정렬
            const dataMap = new Map(itemChartData.data.map(item => {
                const date = new Date(item.date_auction_expire_kst);
                return [date.toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }), item.auction_price_per_unit];
            }));

            dataset.data = chart.data.labels.map(label => dataMap.get(label) || null); // 데이터가 없는 시간대는 null로 처리
        } else {
            dataset.data = Array(chart.data.labels.length).fill(null); // 해당 아이템 데이터가 없으면 모두 null
        }
    });

    chart.update();
};

export const destroyChart = () => {
    if (priceChartInstance) {
        priceChartInstance.destroy();
        priceChartInstance = null;
    }
};
