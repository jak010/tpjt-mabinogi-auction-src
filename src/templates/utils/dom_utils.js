export const getElement = (id) => document.getElementById(id);

export const setTextContent = (elementId, text) => {
    const element = getElement(elementId);
    if (element) {
        element.textContent = text;
    }
};

export const setInputValue = (elementId, value) => {
    const element = getElement(elementId);
    if (element) {
        element.value = value;
    }
};

export const getInputValue = (elementId) => {
    const element = getElement(elementId);
    if (element) {
        return element.value;
    }
    return null;
};

export const addEventListener = (elementId, eventType, handler) => {
    const element = getElement(elementId);
    if (element) {
        element.addEventListener(eventType, handler);
    }
};

export const clearStatistics = () => {
    const statisticsDetailsDiv = getElement('item-statistics-details');
    if (statisticsDetailsDiv) {
        statisticsDetailsDiv.innerHTML = '';
    }
};

export const displayStatistics = (allStatisticsData, onAcquisitionChange) => {
    clearStatistics(); // 기존 통계 정보 초기화
    const statisticsDetailsDiv = getElement('item-statistics-details');

    for (const itemName in allStatisticsData) {
        if (allStatisticsData.hasOwnProperty(itemName)) {
            const statisticsData = allStatisticsData[itemName];
            const itemStatsDiv = document.createElement('div');
            itemStatsDiv.classList.add('item-statistics-card'); // CSS 스타일링을 위한 클래스 추가

            itemStatsDiv.innerHTML = `
                <h3>${itemName}</h3>
                <p><strong>평균 가격:</strong> ${new Intl.NumberFormat('ko-KR').format(statisticsData.average_price)} 골드</p>
                <p><strong>최저 가격:</strong> ${new Intl.NumberFormat('ko-KR').format(statisticsData.min_price)} 골드</p>
                <p><strong>최고 가격:</strong> ${new Intl.NumberFormat('ko-KR').format(statisticsData.max_price)} 골드</p>
                <p><strong>표준 편차:</strong> ${new Intl.NumberFormat('ko-KR').format(statisticsData.standard_deviation)} 골드</p>
                <p><strong>거래량:</strong> ${new Intl.NumberFormat('ko-KR').format(statisticsData.trade_volume)} 건</p>
                <div class="acquisition-input-group">
                    <label for="acquisition-input-${itemName}">30분당 획득 개수:</label>
                    <input type="number" id="acquisition-input-${itemName}" value="0" min="0">
                </div>
                <p><strong>시간당 획득 개수:</strong> <span id="hourly-acquisition-count-${itemName}">0 개</span></p>
                <p><strong>시간당 수익:</strong> <span id="hourly-profit-${itemName}">0 골드</span></p>
            `;
            statisticsDetailsDiv.appendChild(itemStatsDiv);

            // 입력 필드에 이벤트 리스너 추가
            const acquisitionInput = getElement(`acquisition-input-${itemName}`);
            if (acquisitionInput) {
                acquisitionInput.addEventListener('input', (event) => {
                    const count = parseInt(event.target.value, 10);
                    if (!isNaN(count) && onAcquisitionChange) {
                        onAcquisitionChange(itemName, count, statisticsData.average_price);
                    }
                });
            }
            // 초기 계산 및 표시
            if (onAcquisitionChange) {
                onAcquisitionChange(itemName, 0, statisticsData.average_price); // 초기값 0으로 계산
            }
        }
    }
};

export const updateCalculatedStats = (itemName, hourlyAcquisitionCount, hourlyProfit) => {
    setTextContent(`hourly-acquisition-count-${itemName}`, `${hourlyAcquisitionCount} 개`);
    setTextContent(`hourly-profit-${itemName}`, `${new Intl.NumberFormat('ko-KR').format(hourlyProfit)} 골드`);
};
