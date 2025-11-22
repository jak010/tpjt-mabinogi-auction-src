CREATE TABLE locations (
    location_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    code        VARCHAR(100) NOT NULL UNIQUE,
    name        VARCHAR(200) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


CREATE TABLE items (
    item_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    category         VARCHAR(100) NOT NULL,
    name             VARCHAR(200) NOT NULL,
    time_per_minute  INT NOT NULL,
    time_per_count   INT NOT NULL,
    is_searchable    TINYINT NOT NULL DEFAULT 1,
    location_id      BIGINT NOT NULL,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP

) ENGINE=InnoDB;



INSERT INTO locations (code, name) VALUES
('sidhe_finaha', '시드 피나하'),
('tori_canyon', '토리 협곡'),
('paliass', '팔리아스');

INSERT INTO items (
    category, name, time_per_minute, time_per_count, is_searchable, location_id
)
VALUES
('기타', '에코스톤 각성제', 10, 8, 1, (SELECT location_id FROM locations WHERE code='sidhe_finaha')),
('기타', '고급 에코스톤 각성제', 10, 6, 1, (SELECT location_id FROM locations WHERE code='sidhe_finaha')),
('기타', '최고급 에코스톤 각성제', 10, 6, 1, (SELECT location_id FROM locations WHERE code='sidhe_finaha')),
('포션', '크라반의 수액', 10, 12, 1, (SELECT location_id FROM locations WHERE code='tori_canyon')),
('기타', '순수의 결정', 10, 8, 1, (SELECT location_id FROM locations WHERE code='paliass')),
('기타', '붉은 순수의 결정', 10, 8, 1, (SELECT location_id FROM locations WHERE code='paliass'));
('기타', '고급 가죽', 10, 12, 1, (SELECT location_id FROM locations WHERE code='etc'));
('기타', '최고급 가죽', 10, 12, 1, (SELECT location_id FROM locations WHERE code='etc'));
