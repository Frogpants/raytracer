package game.tools;

public class vec2 {
    public double x;
    public double y;

    public vec2(double a, double b) {
        x = a;
        y = b;
    }

    public vec2 add(vec2 b) {
        return new vec2(x + b.x, y + b.y);
    }

    public vec2 sub(vec2 b) {
        return new vec2(x - b.x, y - b.y);
    }

    public vec2 mul(double b) {
        return new vec2(x * b, y * b);
    }

    public vec2 div(double b) {
        return new vec2(x / b, y / b);
    }

    public double dot(vec2 b) {
        return x * b.x + y * b.y;
    }

    public double magnitude() {
        return Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    }
}