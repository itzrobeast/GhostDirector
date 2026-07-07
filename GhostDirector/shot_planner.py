from shot import Shot


class ShotPlanner:

    def create_shots(self, scene):

        shots = []

        shot_duration = scene.duration / 4

        shot_types = [
            "establishing",
            "medium",
            "close_up",
            "hero",
        ]

        for i in range(4):

            shot = Shot(

                shot_number=i + 1,
                scene_number=scene.scene_number,

                start_time=scene.start_time + (i * shot_duration),
                duration=shot_duration,

                shot_type=shot_types[i],

                camera=scene.camera,
                lens=scene.lens,
                movement=scene.movement,

                framing="",
                composition="",

                location=scene.location,
                lighting=scene.lighting,
                weather=scene.weather,
                time_of_day=scene.time_of_day,

                action=scene.action,
                expression=scene.expression,

                prompt="",
            )

            shots.append(shot)

        return shots