let priceChart;
const itemCategories = [
    "무기", "방어구", "장신구", "의류", "소모품", "재료", "도면", "인챈트", "세공", "염색", "악기", "가구", "기타", "천옷/방직"
];
const colors = [
    'rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)',
    'rgb(153, 102, 255)', 'rgb(255, 159, 64)', 'rgb(199, 199, 199)', 'rgb(83, 102, 255)'
];
let itemInputCount = 0;

document.addEventListener('DOMContentLoaded', () => {
    addItemInput('천옷/방직', '고급 가죽');
    addItemInput('기타', '순수의 결정');
    updateAddItemButtonState();
    fetchAndRenderChart(); // 페이지 로드 시 초기 차트 렌더링
    setInterval(fetchAndRenderChart, 15 * 60 * 1000); // 15분마다 업데이트 (15분 * 60초/분 * 1000ms/초)
});

function updateAddItemButtonState() {
    const addItemButton = document.querySelector('button[onclick="addItemInput()"]');
    if (document.querySelectorAll('.item-input-group').length >= 2) {
        addItemButton.style.display = 'none';
    } else {
        addItemButton.style.display = 'block';
    }
}

function addItemInput(defaultCategory = '', defaultName = '') {
    if (document.querySelectorAll('.item-input-group').length >= 2) {
        return; // Do not add more than 2 items
    }
    itemInputCount++;
    const itemInputsDiv = document.getElementById('itemInputs');
    const newItemDiv = document.createElement('div');
    newItemDiv.classList.add('item-input-group');
    newItemDiv.id = `item-group-${itemInputCount}`;

    let optionsHtml = itemCategories.map(category => `<option value="${category}" ${category === defaultCategory ? 'selected' : ''}>${category}</option>`).join('');

    newItemDiv.innerHTML = `
        <div class="input-group">
            <label for="itemCategory-${itemInputCount}">아이템 카테고리:</label>
            <select id="itemCategory-${itemInputCount}">
                ${optionsHtml}
            </select>
        </div>
        <div class="input-group">
            <label for="itemName-${itemInputCount}">아이템 이름:</label>
            <input type="text" id="itemName-${itemInputCount}" placeholder="아이템 이름을 입력하세요 (예: 켈틱 드루이드 스태프)" value="${defaultName}">
            <button onclick="removeItemInput(${itemInputCount})" style="width: auto; padding: 5px 10px; background-color: #dc3545;">삭제</button>
        </div>
    `;
    itemInputsDiv.appendChild(newItemDiv);
    updateAddItemButtonState();
}

function removeItemInput(id) {
    const itemGroup = document.getElementById(`item-group-${id}`);
    if (itemGroup) {
        itemGroup.remove();
    }
    // If all inputs are removed, add one back to prevent empty state
    if (document.querySelectorAll('.item-input-group').length === 0) {
        addItemInput();
    }
    updateAddItemButtonState();
}

async function fetchAndRenderChart() {
    const loadingDiv = document.getElementById('loading');
    const errorMessageDiv = document.getElementById('error-message');

    errorMessageDiv.style.display = 'none';
    errorMessageDiv.textContent = ''; // Clear previous error messages
    loadingDiv.style.display = 'block';

    const itemGroups = document.querySelectorAll('.item-input-group');
    if (itemGroups.length === 0) {
        errorMessageDiv.textContent = '비교할 아이템을 최소 하나 이상 추가해주세요.';
        errorMessageDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        return;
    }

    const itemCategories = [];
    const itemNames = [];

    for (let i = 0; i < itemGroups.length; i++) {
        const id = itemGroups[i].id.split('-')[2];
        const itemCategory = document.getElementById(`itemCategory-${id}`).value;
        const itemName = document.getElementById(`itemName-${id}`).value;

        if (!itemName) {
            errorMessageDiv.textContent = `아이템 이름을 입력해주세요. (아이템 ${i + 1})`;
            errorMessageDiv.style.display = 'block';
            loadingDiv.style.display = 'none';
            return;
        }
        itemCategories.push(itemCategory);
        itemNames.push(itemName);
    }

    const queryParams = new URLSearchParams();
    itemCategories.forEach(cat => queryParams.append('item_category', cat));
    itemNames.forEach(name => queryParams.append('item_name', name));

    try {
        const response = await fetch(`/market/chart-data?${queryParams.toString()}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        const { item_data, item_statistics, recommendation } = await response.json();
        loadingDiv.style.display = 'none';

        const datasets = [];
        const allTimestamps = new Set();

        // Collect all unique timestamps from all items
        Object.values(item_data).forEach(items => {
            items.forEach(item => {
                allTimestamps.add(new Date(item.date_auction_expire).getTime());
            });
        });
        const sortedAllTimestamps = Array.from(allTimestamps).sort((a, b) => a - b);

        // Create datasets, aligning data with sortedAllTimestamps
        let colorIndex = 0;
        for (const itemName in item_data) {
            const data = item_data[itemName];
            const priceMap = new Map();
            data.forEach(item => {
                const itemTimestamp = new Date(item.date_auction_expire).getTime();
                priceMap.set(itemTimestamp, item.auction_price_per_unit);
            });

            const alignedPrices = sortedAllTimestamps.map(ts => {
                const price = priceMap.get(ts);
                return price !== undefined ? price : null; // Use null for missing data points
            });

            const color = colors[colorIndex % colors.length];
            colorIndex++;

            datasets.push({
                label: `${itemName} - 최저 가격 (골드)`,
                data: alignedPrices,
                borderColor: color,
                tension: 0.1,
                fill: false,
                spanGaps: true, // Connect gaps for missing values
                yAxisID: 'y'
            });
        }

        if (datasets.length === 0) {
            errorMessageDiv.textContent = '선택된 아이템에 대한 유효한 데이터를 찾을 수 없습니다.';
            errorMessageDiv.style.display = 'block';
            return;
        }

        // Explicitly destroy any existing chart associated with the canvas before creating a new one
        const existingChart = Chart.getChart('priceChart');
        if (existingChart) {
            existingChart.destroy();
        }
        priceChart = null; // Clear the global reference

        const ctx = document.getElementById('priceChart').getContext('2d');
        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: sortedAllTimestamps, // Use all unique timestamps as labels for time scale
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour', // Display unit for x-axis
                            stepSize: 4, // 4-hour intervals
                            tooltipFormat: 'yyyy-MM-dd HH:mm', // Format for tooltips
                            displayFormats: {
                                hour: 'MM-dd HH:mm', // Format for axis labels
                                day: 'yyyy-MM-dd'
                            }
                        },
                        max: sortedAllTimestamps[sortedAllTimestamps.length - 1] + (4 * 60 * 60 * 1000), // Add 4 hours buffer to the last timestamp
                        title: {
                            display: true,
                            text: '시간'
                        },
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                            color: '#666', // Darker tick labels for better contrast
                            font: {
                                size: 10 // Slightly smaller font for better fit
                            },
                            autoSkip: true, // Enable auto-skipping of labels
                            autoSkipPadding: 10, // Add padding between auto-skipped labels
                            align: 'start' // Align ticks to the start of the interval
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)' // Lighter grid lines
                        }
                    },
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: '가격 (골드)'
                        },
                        ticks: {
                            color: '#666', // Darker tick labels
                            callback: function(value) {
                                return new Intl.NumberFormat('ko-KR').format(value); // Format y-axis labels
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)' // Lighter grid lines
                        },
                        suggestedMin: 0, // Ensure the chart starts from 0 or a reasonable minimum
                        suggestedMax: null, // Let Chart.js calculate max, but we can add padding
                        afterDataLimits: function(scale) {
                            // Add 10% padding to the top of the Y-axis
                            const max = scale.max;
                            scale.max = max * 1.1;
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            title: function(context) {
                                return new Date(context[0].parsed.x).toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
                            },
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('ko-KR').format(context.parsed.y);
                                    if (label.includes('최저 가격')) {
                                        label += ' 골드';
                                    }
                                }
                                return label;
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)', // Darker tooltip background
                        titleColor: '#fff', // White title text
                        bodyColor: '#fff', // White body text
                        borderColor: 'rgba(255, 255, 255, 0.5)', // Light border
                        borderWidth: 1,
                        displayColors: true, // Show color box for each dataset
                        boxPadding: 4 // Padding around color box
                    },
                    legend: {
                        display: true,
                        labels: {
                            color: '#333' // Legend label color
                        }
                    }
                },
                elements: {
                    line: {
                        borderWidth: 2 // Thicker lines
                    },
                    point: {
                        radius: 5, // Larger points
                        hoverRadius: 7, // Even larger hover points
                        backgroundColor: 'white', // White point background
                        borderColor: function(context) {
                            return context.dataset.borderColor; // Point border matches line color
                        }
                    }
                }
            }
        });

        // Render statistics and recommendation using data from backend
        renderStatistics(item_statistics, recommendation);

    } catch (error) {
        loadingDiv.style.display = 'none';
        errorMessageDiv.textContent = `데이터를 불러오는 데 실패했습니다: ${error.message}`;
        errorMessageDiv.style.display = 'block';
        console.error('Error fetching data:', error);
    }
}

function renderStatistics(itemStatistics, recommendationText) {
    const itemStatisticsDiv = document.getElementById('item-statistics');
    const recommendationDiv = document.getElementById('recommendation');
    itemStatisticsDiv.innerHTML = ''; // Clear previous statistics
    recommendationDiv.innerHTML = ''; // Clear previous recommendation

    itemStatistics.forEach(stats => {
        itemStatisticsDiv.innerHTML += `
            <div style="margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                <h3>${stats.itemName}</h3>
                ${stats.error ? `<p style="color: red;">${stats.error}</p>` : `
                    <p>등록된 총 아이템 수: ${new Intl.NumberFormat('ko-KR').format(stats.totalItems)}</p>
                    <p>전체 평균 가격: ${new Intl.NumberFormat('ko-KR').format(stats.averagePrice)} 골드</p>
                    <p>시간별 최저가 평균: ${new Intl.NumberFormat('ko-KR').format(stats.timeBasedAveragePrice)} 골드</p>
                    <p>최저 가격: ${new Intl.NumberFormat('ko-KR').format(stats.minPrice)} 골드</p>
                    <p>최고 가격: ${new Intl.NumberFormat('ko-KR').format(stats.maxPrice)} 골드</p>
                `}
        `;

        if (stats.acquisitionRatePer30Min > 0) {
            itemStatisticsDiv.innerHTML += `
                <p style="font-weight: bold; color: #28a745;">30분당 획득량: ${stats.acquisitionRatePer30Min}개</p>
                <p style="font-weight: bold; color: #28a745;">시간당 예상 수익: ${new Intl.NumberFormat('ko-KR').format(stats.profitPerHour)} 골드</p>
            `;
        }
        itemStatisticsDiv.innerHTML += `</div>`; // Close the div for each item
    });

    recommendationDiv.innerHTML = recommendationText;
}
