#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include <vector>
#include <cmath>

#define WIDTH 800
#define HEIGHT 600
#define NUM_JOSHES 5

struct Josh {
    sf::Sprite sprite;
    sf::Vector2f increment;

    Josh(const sf::Texture& texture, const sf::Vector2f& startPos, const sf::Vector2f& startIncrement) {
        sprite.setTexture(texture);
        sprite.setOrigin(texture.getSize().x / 2, texture.getSize().y / 2);
        sprite.setPosition(startPos);
        increment = startIncrement;
    }

    void move(const sf::Vector2u& windowSize) {
        if ((sprite.getPosition().x + (sprite.getLocalBounds().width / 2) > windowSize.x && increment.x > 0) ||
            (sprite.getPosition().x - (sprite.getLocalBounds().width / 2) < 0 && increment.x < 0)) {
            increment.x = -increment.x;
        }

        if ((sprite.getPosition().y + (sprite.getLocalBounds().height / 2) > windowSize.y && increment.y > 0) ||
            (sprite.getPosition().y - (sprite.getLocalBounds().height / 2) < 0 && increment.y < 0)) {
            increment.y = -increment.y;
        }

        sprite.move(increment);
    }

    bool checkCollision(const Josh& other) const {
        sf::FloatRect bounds1 = sprite.getGlobalBounds();
        sf::FloatRect bounds2 = other.sprite.getGlobalBounds();
        return bounds1.intersects(bounds2);
    }

    bool checkCollision(const sf::CircleShape& circle) const {
        sf::FloatRect bounds1 = sprite.getGlobalBounds();
        sf::FloatRect bounds2 = circle.getGlobalBounds();
        return bounds1.intersects(bounds2);
    }
};

void zoomOut(sf::RenderWindow* window, unsigned int frame) {
    float multiplier = 950.0;

    sf::View view = window->getView();
    view.setSize(sf::Vector2f(1.1*WIDTH - (WIDTH * multiplier / frame), 1.1*HEIGHT - (HEIGHT * multiplier / frame)));
    window->setView(view);
}

sf::Color rainbowColor(float t) {
    // Используем функцию sin для создания радужных цветов
    float frequency = 0.01f;
    int r = static_cast<int>(sin(frequency * t + 0) * 127 + 128);
    int g = static_cast<int>(sin(frequency * t + 2) * 127 + 128);
    int b = static_cast<int>(sin(frequency * t + 4) * 127 + 128);
    return sf::Color(r, g, b, 2);
}

int main() {
    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "Whistle baby", 0b100);

    sf::Image icon;
    icon.loadFromFile("../ext/images/josh.png");
    window.setIcon(icon.getSize().x, icon.getSize().y, icon.getPixelsPtr());

    sf::Texture JoshTexture;
    JoshTexture.loadFromFile("../ext/images/josh.png");

    sf::Music music;
    music.openFromFile("../ext/sound/whistle.wav");
    music.setVolume(50.f);
    music.setPitch(1.1f);
    music.play();

    sf::Text text;
    sf::Font font;
    font.loadFromFile("../ext/font/LuckiestGuy.ttf");
    text.setFont(font);
    text.setString("Whistle baby");
    text.setCharacterSize(24);
    text.setStyle(sf::Text::Bold | sf::Text::Underlined);
    text.setPosition((WIDTH / 2) - 90,  (HEIGHT / 2) - 160);
    text.setOutlineThickness(.6f);

    std::vector<Josh> joshes;
    for (int i = 0; i < NUM_JOSHES; ++i) {
        auto x = static_cast<float>(rand() % WIDTH);
        auto y = static_cast<float>(rand() % HEIGHT);
        float dx = static_cast<float>(rand() % 10 - 5) / 10.0f;
        float dy = static_cast<float>(rand() % 10 - 5) / 10.0f;
        joshes.emplace_back(JoshTexture, sf::Vector2f(x, y), sf::Vector2f(dx, dy));
    }

    sf::CircleShape circleJosh(JoshTexture.getSize().x);
    circleJosh.setOrigin(JoshTexture.getSize().x, JoshTexture.getSize().y);
    circleJosh.setPosition(WIDTH / 2, HEIGHT / 2);
    circleJosh.setTexture(&JoshTexture);
    circleJosh.setTextureRect(sf::IntRect(10, 10, 100, 100));

    unsigned int frame = 1;

    while (window.isOpen()) {
        ++frame;
        sf::Event event{};

        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }

        zoomOut(&window, frame);
        circleJosh.rotate(0.1f);

        for (auto& josh : joshes) {
            josh.move(window.getSize());
        }

        for (size_t i = 0; i < joshes.size(); ++i) {
            for (size_t j = i + 1; j < joshes.size(); ++j) {
                if (joshes[i].checkCollision(joshes[j])) {
                    // Обработка столкновения между joshes[i] и joshes[j]
                    joshes[i].increment = -joshes[i].increment;
                    joshes[j].increment = -joshes[j].increment;
                }
            }
        }

        // Проверяем столкновение круга с josh'ами
        for (auto& josh : joshes) {
            if (josh.checkCollision(circleJosh)) {
                // Обработка столкновения между josh и кругом
                josh.increment = -josh.increment;
            }
        }

        // Создаем градиент радуги в качестве фона и заливки текста
        sf::RectangleShape background(sf::Vector2f(WIDTH, HEIGHT));
        for (int i = 0; i < WIDTH; ++i) {
            background.setFillColor(rainbowColor(frame + i));
            window.draw(background);
        }

        text.setFillColor(background.getFillColor());

        for (const auto& josh : joshes) {
            window.draw(josh.sprite);
        }

        window.draw(circleJosh);
        window.draw(text);
        window.display();
    }

    return 0;
}
