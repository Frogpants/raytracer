package game;

import game.tools.Transform;
import game.tools.vec3;

public class Camera {
    public Camera() {
        Transform transform = new Transform(new vec3(0, 0, 0), new vec3(0, 0, 0));
    }
}
