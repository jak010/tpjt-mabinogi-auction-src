import { fetchChartData, fetchStatisticsData } from './services/api_service.js';
import { getElement, setTextContent, addEventListener, clearStatistics, displayStatistics, updateCalculatedStats } from './utils/dom_utils.js';
import { initializeChart, updateChart, destroyChart } from './chart/price_chart.js';

document.addEventListener('DOMContentLoaded', () => {
    const itemNameInput = getElement('item-name-input');
    const addItemButton = getElement('add-item-button');
    const compareItemsButton = getElement('compare-items-button');
    const selectedItemsList = getElement('selected-items-list');
    const errorMessageDiv = getElement('error-message');
    const ctx = getElement('priceChart').getContext('2d');
    let priceChart;
    let selectedItems = []; // 선택된 아이템들을 저장할 배열
    let itemStatisticsCache = {}; // 아이템별 통계 데이터를 저장할 캐시

    const renderSelectedItems = () => {
        selectedItemsList.innerHTML = ''; // 목록 초기화
        selectedItems.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = item;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.classList.add('remove-item-button');
            removeButton.addEventListener('click', () => {
                selectedItems = selectedItems.filter(selected => selected !== item);
                delete itemStatisticsCache[item]; // 캐시에서도 제거
                renderSelectedItems(); // 목록 다시 렌더링
                if (selectedItems.length === 0) {
                    destroyChart();
                    clearStatistics();
                } else {
                    // 아이템 제거 후 통계 및 차트 다시 그리기
                    fetchDataAndDrawChart();
                }
            });
            listItem.appendChild(removeButton);
            selectedItemsList.appendChild(listItem);
        });
    };

    const addSelectedItem = () => {
        const itemName = itemNameInput.value.trim();
        if (itemName && !selectedItems.includes(itemName)) {
            selectedItems.push(itemName);
            itemNameInput.value = ''; // 입력 필드 초기화
            setTextContent('error-message', ''); // 에러 메시지 초기화
            renderSelectedItems();
        } else if (selectedItems.includes(itemName)) {
            setTextContent('error-message', '이미 추가된 아이템입니다.');
        } else {
            setTextContent('error-message', '아이템 이름을 입력해주세요.');
        }
    };

    // 획득 개수 변경 시 시간당 획득률 및 수익 계산 함수
    const calculateAndDisplayProfit = (itemName, acquisitionCount, averagePrice) => {
        // 30분당 획득 개수를 시간당으로 변환 (30분 * 2 = 1시간)
        const hourlyAcquisitionCount = acquisitionCount * 2;
        // 시간당 수익 = 시간당 획득 개수 * 평균 가격
        const hourlyProfit = hourlyAcquisitionCount * averagePrice;

        updateCalculatedStats(itemName, hourlyAcquisitionCount, hourlyProfit);
    };

    const fetchDataAndDrawChart = async () => {
        if (selectedItems.length === 0) {
            setTextContent('error-message', '비교할 아이템을 하나 이상 추가해주세요.');
            destroyChart();
            clearStatistics();
            return;
        }

        setTextContent('error-message', ''); // Clear previous errors
        destroyChart(); // 기존 차트 파괴

        const allChartData = [];
        const currentStatisticsData = {}; // 현재 요청에 대한 통계 데이터

        for (const itemName of selectedItems) {
            try {
                // 캐시에 데이터가 없으면 API 호출
                if (!itemStatisticsCache[itemName]) {
                    const chartData = await fetchChartData(itemName);
                    if (chartData.length === 0) {
                        setTextContent('error-message', `${itemName}에 대한 데이터가 없습니다.`);
                        continue; // 다음 아이템으로 넘어감
                    }
                    allChartData.push({ itemName, data: chartData });

                    const statisticsData = await fetchStatisticsData(itemName);
                    itemStatisticsCache[itemName] = statisticsData; // 캐시에 저장
                } else {
                    // 캐시에 데이터가 있으면 캐시된 데이터 사용
                    allChartData.push({ itemName, data: await fetchChartData(itemName) }); // 차트 데이터는 매번 새로 가져오는 것이 좋을 수 있음 (최신 데이터 반영)
                }
                currentStatisticsData[itemName] = itemStatisticsCache[itemName];

            } catch (error) {
                console.error(`'${itemName}' 데이터를 불러오는 중 오류 발생:`, error);
                setTextContent('error-message', `'${itemName}' 데이터를 불러오지 못했습니다: ${error.message}`);
                // 특정 아이템 오류 시에도 다른 아이템은 계속 처리
            }
        }

        if (allChartData.length === 0) {
            setTextContent('error-message', '선택된 아이템 중 유효한 데이터를 찾을 수 없습니다.');
            destroyChart();
            clearStatistics();
            return;
        }

        // 차트 초기화 및 업데이트 (여러 데이터셋 처리)
        priceChart = initializeChart(ctx, allChartData.map(d => d.itemName)); // 차트 제목에 모든 아이템 이름 포함
        updateChart(priceChart, allChartData); // 여러 데이터셋을 처리하도록 updateChart 수정 필요

        // 통계 정보 표시 (여러 아이템 통계 처리)
        // displayStatistics 함수에 calculateAndDisplayProfit 콜백 전달
        displayStatistics(currentStatisticsData, calculateAndDisplayProfit);
    };

    addEventListener('add-item-button', 'click', addSelectedItem);
    addEventListener('compare-items-button', 'click', fetchDataAndDrawChart);

    // 엔터 키로 아이템 추가
    itemNameInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addSelectedItem();
        }
    });
});
