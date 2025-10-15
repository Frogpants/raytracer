package game.tools;

public class Transform {
    public vec3 position;
    public vec3 rotation;

    public Transform(vec3 pos, vec3 rot) {
        position = new vec3(pos.x, pos.y, pos.z);
        rotation = new vec3(rot.x, rot.y, rot.z);
    }
}

