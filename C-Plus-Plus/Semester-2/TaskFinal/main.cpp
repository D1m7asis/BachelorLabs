#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>

#define WIDTH 1600
#define HEIGHT 900

float G = 9.81/.04f;
#define DAMPING 0.65
#define HORIZONTAL_DAMPING 0.99996f
#define SPHERE_DRAG_COEF 0.5
#define AIR_DENSITY 1.3
#define GROUND_HEIGHT 780

class Ball {
public:
    sf::CircleShape ball;
    float vx = 0;
    float vy = 0;
    float radius;

    Ball(float radius, float pos_x, float pos_y) : radius(radius) {
        sf::Texture ballTexture;
        ballTexture.loadFromFile("../ext/ball.jpg");

        ball.setRadius(radius);
        ball.setOrigin(sf::Vector2f(radius, radius));
        ball.setPosition(pos_x, pos_y);
        ball.setTexture(&ballTexture);
    }

    void update(float t) {
        float acceleration = G * (2 - 1 / (1 + calculateAirResistance()));

        vy += acceleration * t;
        vx = vx * HORIZONTAL_DAMPING;

        ball.move(0, vy * t);
        ball.move(vx * t, 0);

        check_border_collision();
    }

    void check_border_collision() {
        if (ball.getPosition().y + ball.getRadius() >= GROUND_HEIGHT) { // UP
            ball.setPosition(ball.getPosition().x, GROUND_HEIGHT - ball.getRadius());
            vy = -vy * DAMPING;
        }

        if (ball.getPosition().y - ball.getRadius() <= 0) { // DOWN
            ball.setPosition(ball.getPosition().x, ball.getRadius());
            vy = -vy * DAMPING;
        }

        if (ball.getPosition().x + ball.getRadius() >= WIDTH) {
            ball.setPosition(WIDTH - ball.getRadius(), ball.getPosition().y);
            vx = -vx * DAMPING;
        }

        if (ball.getPosition().x - ball.getRadius() <= 0) {
            ball.setPosition(ball.getRadius(), ball.getPosition().y);
            vx = -vx * DAMPING;
        }
    }

    float calculateAirResistance() const {
        float SphereArea = 3.14f * radius * radius;
        float current_speed = sqrt(vy * vy + vx * vx);
        float AirResistance = (SPHERE_DRAG_COEF * SphereArea * AIR_DENSITY * (current_speed / 100.f) * (current_speed / 100.f)) / 2.f;
        return AirResistance / 30000.f;
    }

};

int main() {
    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "Bouncy balls");

    std::vector<Ball> balls;
    sf::Texture ballTexture;
    ballTexture.loadFromFile("../ext/ball.jpg");

    float r1 = 50.f;
    float r2 = 100.f;
    float r3 = 150.f;
    balls.emplace_back(r1, 100.f, 2*r3-r1).ball.setTexture(&ballTexture);
    balls.emplace_back(r2, 500.f, 2*r3-r2).ball.setTexture(&ballTexture);
    balls.emplace_back(r3, 1000.f, r3).ball.setTexture(&ballTexture);

    //balls[0].vx = r1;
    //balls[1].vx = r2;
    //balls[2].vx = r3;

    sf::RectangleShape background(sf::Vector2f(WIDTH, HEIGHT));
    sf::Texture sky;
    sky.loadFromFile("../ext/sky.jpg");
    background.setTexture(&sky);

    sf::RectangleShape ground(sf::Vector2f(WIDTH, 300));
    sf::Texture grass;
    grass.loadFromFile("../ext/grass.jpg");
    ground.setTexture(&grass);
    ground.setPosition(0, GROUND_HEIGHT);

    sf::RectangleShape mouse(sf::Vector2f(100, 100));
    sf::Texture mouse_texture;
    mouse_texture.loadFromFile("../ext/mouse.png");
    mouse.setTexture(&mouse_texture);
    mouse.setPosition(WIDTH-mouse.getSize().x, 0);

    sf::RectangleShape arrow(sf::Vector2f(200, 100));
    sf::Texture arrow_texture;
    arrow.rotate(-90);
    arrow_texture.loadFromFile("../ext/arrow.jpg");
    arrow.setTexture(&arrow_texture);
    arrow.setPosition(WIDTH-arrow.getSize().y / 2, mouse.getSize().y + arrow.getSize().y);
    arrow.setOrigin(arrow.getSize().x/2, arrow.getSize().y/2);

    sf::Clock clock;
    bool lock_click = false;

    while (window.isOpen()) {
        sf::Event event{};
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        float t = clock.restart().asSeconds();

        for (auto& ball : balls) {
            ball.update(t);
        }

        if (sf::Mouse::isButtonPressed(sf::Mouse::Left) && !lock_click) {
            G = -G;
            arrow.rotate(180);
            lock_click = true;
        }

        if (event.type == sf::Event::MouseButtonReleased)  {
            if (event.mouseButton.button == sf::Mouse::Left) {
                lock_click = false;
            }
        }

        window.clear();
        window.draw(background);
        window.draw(ground);
        window.draw(mouse);
        window.draw(arrow);

        for (const auto& ball : balls) {
            window.draw(ball.ball);
        }

        window.display();
    }
}