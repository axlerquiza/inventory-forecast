USE inventory;

-- Insert unit types
INSERT INTO unit_types (name, description) VALUES 
('Unit', 'Single item'),
('Bundle', 'Packaged items')
ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description);

-- Insert categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Furniture', 'Home and office furniture'),
('Groceries', 'Daily grocery items'),
ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description);
