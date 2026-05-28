-- ============================================================
--  RECIPE DATABASE SEED SCRIPT — PostgreSQL
--  Tables: core_recipe, core_tag, core_ingredients,
--          core_recipe_tag, core_recipe_ingredient
-- ============================================================

BEGIN;

-- ------------------------------------------------------------
--  CLEAN SLATE
-- ------------------------------------------------------------
TRUNCATE core_recipe_ingredient, core_recipe_tag, core_ingredients, core_tag, core_recipe
  RESTART IDENTITY CASCADE;

-- ============================================================
--  TAGS (shared across recipes)
-- ============================================================
INSERT INTO core_tag (name, user_id, created_at, updated_at) VALUES
  ('Italian',    1, NOW(), NOW()),   -- 1
  ('Pasta',      1, NOW(), NOW()),   -- 2
  ('Quick',      1, NOW(), NOW()),   -- 3
  ('Indian',     1, NOW(), NOW()),   -- 4
  ('Curry',      1, NOW(), NOW()),   -- 5
  ('Spicy',      1, NOW(), NOW()),   -- 6
  ('Breakfast',  1, NOW(), NOW()),   -- 7
  ('Vegetarian', 1, NOW(), NOW()),   -- 8
  ('Mexican',    1, NOW(), NOW()),   -- 9
  ('Street food',1, NOW(), NOW()),   -- 10
  ('Greek',      1, NOW(), NOW()),   -- 11
  ('Salad',      1, NOW(), NOW()),   -- 12
  ('Vegan',      1, NOW(), NOW()),   -- 13
  ('No-cook',    1, NOW(), NOW()),   -- 14
  ('Pizza',      1, NOW(), NOW()),   -- 15
  ('Thai',       1, NOW(), NOW()),   -- 16
  ('Noodles',    1, NOW(), NOW()),   -- 17
  ('Seafood',    1, NOW(), NOW()),   -- 18
  ('Dessert',    1, NOW(), NOW()),   -- 19
  ('Chocolate',  1, NOW(), NOW()),   -- 20
  ('Baking',     1, NOW(), NOW()),   -- 21
  ('American',   1, NOW(), NOW()),   -- 22
  ('Classic',    1, NOW(), NOW()),   -- 23
  ('Healthy',    1, NOW(), NOW());   -- 24

-- ============================================================
--  INGREDIENTS (shared across recipes)
-- ============================================================
INSERT INTO core_ingredients (name, user_id, created_at, updated_at) VALUES
  ('Spaghetti',           1, NOW(), NOW()),   -- 1
  ('Guanciale',           1, NOW(), NOW()),   -- 2
  ('Eggs',                1, NOW(), NOW()),   -- 3
  ('Pecorino Romano',     1, NOW(), NOW()),   -- 4
  ('Black pepper',        1, NOW(), NOW()),   -- 5
  ('Chicken',             1, NOW(), NOW()),   -- 6
  ('Yogurt',              1, NOW(), NOW()),   -- 7
  ('Tomatoes',            1, NOW(), NOW()),   -- 8
  ('Cream',               1, NOW(), NOW()),   -- 9
  ('Garam masala',        1, NOW(), NOW()),   -- 10
  ('Ginger',              1, NOW(), NOW()),   -- 11
  ('Garlic',              1, NOW(), NOW()),   -- 12
  ('Sourdough',           1, NOW(), NOW()),   -- 13
  ('Avocado',             1, NOW(), NOW()),   -- 14
  ('Lemon',               1, NOW(), NOW()),   -- 15
  ('Chili flakes',        1, NOW(), NOW()),   -- 16
  ('Ground beef',         1, NOW(), NOW()),   -- 17
  ('Corn tortillas',      1, NOW(), NOW()),   -- 18
  ('Cheddar',             1, NOW(), NOW()),   -- 19
  ('Salsa',               1, NOW(), NOW()),   -- 20
  ('Lettuce',             1, NOW(), NOW()),   -- 21
  ('Lime',                1, NOW(), NOW()),   -- 22
  ('Cucumber',            1, NOW(), NOW()),   -- 23
  ('Red onion',           1, NOW(), NOW()),   -- 24
  ('Feta',                1, NOW(), NOW()),   -- 25
  ('Olives',              1, NOW(), NOW()),   -- 26
  ('Olive oil',           1, NOW(), NOW()),   -- 27
  ('Pizza dough',         1, NOW(), NOW()),   -- 28
  ('San Marzano tomatoes',1, NOW(), NOW()),   -- 29
  ('Mozzarella',          1, NOW(), NOW()),   -- 30
  ('Basil',               1, NOW(), NOW()),   -- 31
  ('Rice noodles',        1, NOW(), NOW()),   -- 32
  ('Shrimp',              1, NOW(), NOW()),   -- 33
  ('Bean sprouts',        1, NOW(), NOW()),   -- 34
  ('Peanuts',             1, NOW(), NOW()),   -- 35
  ('Tamarind',            1, NOW(), NOW()),   -- 36
  ('Fish sauce',          1, NOW(), NOW()),   -- 37
  ('Dark chocolate',      1, NOW(), NOW()),   -- 38
  ('Butter',              1, NOW(), NOW()),   -- 39
  ('Sugar',               1, NOW(), NOW()),   -- 40
  ('Flour',               1, NOW(), NOW()),   -- 41
  ('Vanilla',             1, NOW(), NOW()),   -- 42
  ('Romaine',             1, NOW(), NOW()),   -- 43
  ('Parmesan',            1, NOW(), NOW()),   -- 44
  ('Croutons',            1, NOW(), NOW()),   -- 45
  ('Anchovies',           1, NOW(), NOW()),   -- 46
  ('Worcestershire',      1, NOW(), NOW()),   -- 47
  ('Frozen mango',        1, NOW(), NOW()),   -- 48
  ('Banana',              1, NOW(), NOW()),   -- 49
  ('Coconut milk',        1, NOW(), NOW()),   -- 50
  ('Granola',             1, NOW(), NOW()),   -- 51
  ('Chia seeds',          1, NOW(), NOW()),   -- 52
  ('Berries',             1, NOW(), NOW());   -- 53

-- ============================================================
--  1. SPAGHETTI CARBONARA
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Spaghetti Carbonara',
  'Creamy Roman pasta with eggs, Pecorino Romano, guanciale and black pepper.',
  'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600&q=80',
  25, 12,
  'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Boil pasta","text":"Bring a large pot of salted water to a boil and cook spaghetti until al dente. Reserve 1 cup of pasta water before draining.","timer":600},
    {"step":2,"title":"Render guanciale","text":"In a cold pan add guanciale and cook over medium heat until the fat renders and edges are crispy, about 6-8 minutes. Remove from heat.","timer":420},
    {"step":3,"title":"Make egg mixture","text":"Whisk together eggs, egg yolks, and grated Pecorino Romano in a bowl. Add freshly cracked black pepper generously.","timer":0},
    {"step":4,"title":"Combine","text":"Add hot drained pasta to the pan with guanciale (off heat). Pour egg mixture over, tossing quickly. Add pasta water a splash at a time until silky and creamy.","timer":0},
    {"step":5,"title":"Serve","text":"Plate immediately, topped with extra Pecorino Romano and a crack of fresh black pepper.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (1,1),(1,2),(1,3);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (1,1),(1,2),(1,3),(1,4),(1,5);

-- ============================================================
--  2. CHICKEN TIKKA MASALA
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Chicken Tikka Masala',
  'Tender chicken in a rich, spiced tomato-cream sauce with warming Indian spices.',
  'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80',
  45, 18,
  'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Marinate chicken","text":"Mix chicken cubes with yogurt, half the garam masala, turmeric, and salt. Marinate for at least 30 minutes.","timer":1800},
    {"step":2,"title":"Cook chicken","text":"Grill or pan-sear marinated chicken over high heat until charred at the edges, about 8 minutes. Set aside.","timer":480},
    {"step":3,"title":"Build the base","text":"Heat oil in a large pan. Saute diced onion until golden, 5-6 minutes. Add minced garlic and grated ginger, cook 2 more minutes.","timer":480},
    {"step":4,"title":"Simmer sauce","text":"Add remaining garam masala and crushed tomatoes. Simmer 15 minutes until sauce thickens.","timer":900},
    {"step":5,"title":"Finish and serve","text":"Stir in heavy cream and cooked chicken. Simmer 5 more minutes. Adjust salt and serve with basmati rice or naan.","timer":300}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (2,4),(2,5),(2,6);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (2,6),(2,7),(2,8),(2,9),(2,10),(2,11),(2,12);

-- ============================================================
--  3. AVOCADO TOAST
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Avocado Toast',
  'Smashed avocado on sourdough with chili flakes, lemon and poached eggs.',
  'https://images.unsplash.com/photo-1541519227354-08fa5d50c820?w=600&q=80',
  10, 8,
  'https://images.unsplash.com/photo-1541519227354-08fa5d50c820?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Toast bread","text":"Toast sourdough slices until golden and crisp.","timer":180},
    {"step":2,"title":"Smash avocado","text":"Halve the avocado, scoop flesh into a bowl. Add lemon juice, salt, and black pepper. Smash with a fork - keep it chunky.","timer":0},
    {"step":3,"title":"Poach eggs","text":"Bring a deep pan of water to a gentle simmer. Add a splash of white vinegar. Crack each egg into a small cup and slide in gently. Poach 3 minutes for a runny yolk.","timer":180},
    {"step":4,"title":"Assemble and serve","text":"Spread smashed avocado generously over each toast slice. Top each with a poached egg. Sprinkle chili flakes and extra salt.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (3,7),(3,8),(3,3);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (3,13),(3,14),(3,15),(3,16),(3,3);

-- ============================================================
--  4. BEEF TACOS
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Beef Tacos',
  'Crispy corn tortillas stuffed with seasoned ground beef, salsa, cheese and lime.',
  'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=600&q=80',
  20, 14,
  'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Brown the beef","text":"Heat oil in a skillet over medium-high. Add ground beef and break apart. Cook until browned, about 6 minutes.","timer":360},
    {"step":2,"title":"Season","text":"Add cumin, smoked paprika, garlic powder, and salt to the beef. Stir well and cook 2 more minutes until fragrant.","timer":120},
    {"step":3,"title":"Warm tortillas","text":"Warm corn tortillas in a dry skillet or directly over a flame for 20-30 seconds per side until pliable with light char spots.","timer":60},
    {"step":4,"title":"Assemble and serve","text":"Fill each tortilla with seasoned beef, shredded cheddar, lettuce, and fresh salsa. Squeeze lime over the top and serve.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (4,9),(4,10),(4,3);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (4,17),(4,18),(4,19),(4,20),(4,21),(4,22);

-- ============================================================
--  5. GREEK SALAD
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Greek Salad',
  'Classic Horiatiki with ripe tomatoes, cucumber, Kalamata olives and feta.',
  'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&q=80',
  10, 9,
  'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Layer the vegetables","text":"Arrange tomato wedges and cucumber half-moons in a wide bowl or plate. Scatter thinly sliced red onion over the top.","timer":0},
    {"step":2,"title":"Add olives and feta","text":"Nestle Kalamata olives among the vegetables. Place feta as a whole slab on top - do not crumble.","timer":0},
    {"step":3,"title":"Dress and serve","text":"Drizzle extra virgin olive oil generously over everything. Sprinkle dried oregano, salt, and black pepper. Serve immediately.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (5,11),(5,12),(5,13),(5,14);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (5,8),(5,23),(5,24),(5,25),(5,26),(5,27);

-- ============================================================
--  6. MARGHERITA PIZZA
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Margherita Pizza',
  'Wood-fire-style pizza with San Marzano tomato sauce, fresh mozzarella and basil.',
  'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80',
  30, 11,
  'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Preheat oven","text":"Place a baking stone or heavy tray in the oven and preheat to maximum heat (250-300C) for at least 30 minutes.","timer":1800},
    {"step":2,"title":"Stretch dough","text":"Dust a surface with semolina or flour. Stretch the pizza dough by hand into a thin 30cm round - do not use a rolling pin.","timer":0},
    {"step":3,"title":"Spread sauce","text":"Season crushed San Marzano tomatoes with salt and a drizzle of olive oil. Spread thinly over the dough, leaving a 2cm border.","timer":0},
    {"step":4,"title":"Top and bake","text":"Scatter torn fresh mozzarella evenly over the sauce. Slide onto the hot stone and bake 8-10 minutes until crust is charred and cheese is bubbling.","timer":540},
    {"step":5,"title":"Finish and serve","text":"Remove from oven. Scatter fresh basil leaves and finish with a drizzle of olive oil. Slice and serve.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (6,1),(6,15),(6,8);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (6,28),(6,29),(6,30),(6,31),(6,27);

-- ============================================================
--  7. PAD THAI
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Pad Thai',
  'Stir-fried rice noodles with shrimp, egg, bean sprouts, peanuts and tamarind.',
  'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=600&q=80',
  25, 13,
  'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Soak noodles","text":"Soak flat rice noodles in warm water for 20 minutes until pliable but not fully soft. Drain and set aside.","timer":1200},
    {"step":2,"title":"Make sauce","text":"Mix tamarind paste, fish sauce, and palm sugar in a small bowl. Taste and adjust sweet/sour/salty balance.","timer":0},
    {"step":3,"title":"Cook shrimp","text":"Heat oil in a wok over high heat until smoking. Stir-fry minced garlic for 30 seconds. Add shrimp and cook 2 minutes until pink.","timer":150},
    {"step":4,"title":"Scramble eggs","text":"Push shrimp to the side. Crack eggs into the wok and scramble lightly, then mix with the shrimp.","timer":0},
    {"step":5,"title":"Stir-fry noodles","text":"Add drained noodles and pour sauce over. Toss vigorously on high heat for 2-3 minutes until noodles are coated and slightly caramelised.","timer":180},
    {"step":6,"title":"Finish and serve","text":"Add bean sprouts and chopped spring onions, toss briefly. Plate and top with crushed roasted peanuts. Serve with lime wedges.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (7,16),(7,17),(7,18);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (7,32),(7,33),(7,3),(7,34),(7,35),(7,36),(7,37);

-- ============================================================
--  8. CHOCOLATE LAVA CAKE
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Chocolate Lava Cake',
  'Warm dark-chocolate cakes with a molten gooey centre, served with vanilla ice cream.',
  'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80',
  20, 10,
  'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Prepare ramekins","text":"Preheat oven to 200C. Butter 4 ramekins and dust with cocoa powder, tapping out any excess.","timer":0},
    {"step":2,"title":"Melt chocolate","text":"Melt dark chocolate and butter together in a heatproof bowl over simmering water (or microwave in 30-second bursts). Stir until smooth. Let cool slightly.","timer":300},
    {"step":3,"title":"Whisk eggs","text":"In a separate bowl, whisk eggs, egg yolks, and caster sugar until pale and slightly thickened, about 3 minutes.","timer":180},
    {"step":4,"title":"Combine batter","text":"Fold the chocolate mixture into the egg mixture. Sift in plain flour and fold gently until just combined. Add vanilla extract.","timer":0},
    {"step":5,"title":"Bake","text":"Pour batter evenly into the prepared ramekins. Bake 10-12 minutes - the edges should be set but the centre should still wobble.","timer":660},
    {"step":6,"title":"Unmould and serve","text":"Run a knife around the edge of each ramekin and invert onto a plate. Serve immediately with a scoop of vanilla ice cream.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (8,19),(8,20),(8,21);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (8,38),(8,39),(8,3),(8,40),(8,41),(8,42);

-- ============================================================
--  9. CAESAR SALAD
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Caesar Salad',
  'Romaine lettuce, house-made Caesar dressing, croutons and shaved Parmesan.',
  'https://images.unsplash.com/photo-1512852939750-1305098529bf?w=600&q=80',
  15, 10,
  'https://images.unsplash.com/photo-1512852939750-1305098529bf?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Make the croutons","text":"Preheat oven to 200C. Toss cubed sourdough with olive oil and a pinch of salt. Spread on a baking tray in a single layer.","timer":0},
    {"step":2,"title":"Bake croutons","text":"Bake for 12-15 minutes, turning once halfway, until golden and crunchy. Remove and let cool.","timer":840},
    {"step":3,"title":"Make the dressing base","text":"Using a mortar and pestle (or the flat of a knife), mash garlic cloves and anchovy fillets into a smooth paste.","timer":0},
    {"step":4,"title":"Emulsify the dressing","text":"Whisk together the anchovy-garlic paste, egg yolk, Dijon mustard, lemon juice, and Worcestershire sauce. Slowly drizzle in extra virgin olive oil while whisking constantly until creamy and emulsified.","timer":0},
    {"step":5,"title":"Prep the lettuce","text":"Tear or chop romaine hearts into bite-sized pieces. Rinse under cold water and spin or pat completely dry.","timer":0},
    {"step":6,"title":"Toss and serve","text":"Add romaine to a large bowl. Pour over the dressing and toss well to coat every leaf. Add croutons and half the shaved Parmesan, toss gently. Plate and top with remaining Parmesan and a crack of fresh black pepper.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (9,22),(9,12),(9,23);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (9,43),(9,44),(9,45),(9,46),(9,12),(9,15),(9,47);

-- ============================================================
--  10. MANGO SMOOTHIE BOWL
-- ============================================================
INSERT INTO core_recipe (title, description, image, time_minutes, price, link, user_id, created_at, updated_at, recipe_procedure)
VALUES (
  'Mango Smoothie Bowl',
  'Thick blended mango base topped with granola, fresh fruit and chia seeds.',
  'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=600&q=80',
  8, 7,
  'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=600&q=80',
  1, NOW(), NOW(),
  '[
    {"step":1,"title":"Blend the base","text":"Add frozen mango chunks, frozen banana, and coconut milk to a high-speed blender. Blend until completely smooth and very thick, adding more coconut milk only if needed. Squeeze in lime juice and add honey or agave if desired.","timer":0},
    {"step":2,"title":"Pour into bowl","text":"Pour the thick mango base into a wide bowl.","timer":0},
    {"step":3,"title":"Add toppings and serve","text":"Arrange granola, mixed fresh berries, and chia seeds in neat sections over the top. Serve immediately before the base softens.","timer":0}
  ]'::jsonb
);

INSERT INTO core_recipe_tag (recipe_id, tag_id) VALUES (10,7),(10,13),(10,24);
INSERT INTO core_recipe_ingredient (recipe_id, ingredients_id) VALUES (10,48),(10,49),(10,50),(10,51),(10,52),(10,53);

-- ------------------------------------------------------------
--  VERIFICATION
-- ------------------------------------------------------------
SELECT
  r.id,
  r.title,
  r.time_minutes,
  r.price,
  r.user_id,
  jsonb_array_length(r.recipe_procedure) AS procedure_steps,
  COUNT(DISTINCT rt.tag_id)              AS tag_count,
  COUNT(DISTINCT ri.ingredients_id)      AS ingredient_count
FROM core_recipe r
LEFT JOIN core_recipe_tag        rt ON rt.recipe_id = r.id
LEFT JOIN core_recipe_ingredient ri ON ri.recipe_id = r.id
GROUP BY r.id, r.title, r.time_minutes, r.price, r.user_id, r.recipe_procedure
ORDER BY r.id;

COMMIT;
