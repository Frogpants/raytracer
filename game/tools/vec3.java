package game.tools;

public class vec3 {
    public double x;
    public double y;
    public double z;

    public vec3(double a, double b, double c) {
        x = a;
        y = b;
        z = c;
    }

    public vec3 add(vec3 b) {
        return new vec3(x + b.x, y + b.y, z + b.z);
    }

    public vec3 sub(vec3 b) {
        return new vec3(x - b.x, y - b.y, z - b.z);
    }

    public vec3 mul(double b) {
        return new vec3(x * b, y * b, z * b);
    }

    public vec3 div(double b) {
        return new vec3(x / b, y / b, z / b);
    }

    public double dot(vec3 b) {
        return x * b.x + y * b.y + z * b.z;
    }

    public vec3 cross(vec3 b) {
        return new vec3(
            y * b.z - z * b.y,
            z * b.x - x * b.z,
            x * b.y - y * b.x
        );
    }

    public double magnitude() {
        return Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2) + Math.pow(z, 2));
    }
}