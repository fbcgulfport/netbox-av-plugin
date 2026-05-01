from dcim.models import FrontPort, Interface, RearPort
from extras.validators import CustomValidator

from .choices import AVDirectionChoices
from .models import AVPortAssignment


class AVCableValidator(CustomValidator):
    def validate(self, instance, request):
        if not instance.a_terminations or not instance.b_terminations:
            return

        if len(instance.a_terminations) != 1 or len(instance.b_terminations) != 1:
            return

        endpoint_a = instance.a_terminations[0]
        endpoint_b = instance.b_terminations[0]
        if not isinstance(endpoint_a, (Interface, FrontPort, RearPort)):
            return
        if not isinstance(endpoint_b, (Interface, FrontPort, RearPort)):
            return

        if isinstance(endpoint_a, Interface):
            kwargs_a = {"interface": endpoint_a}
        elif isinstance(endpoint_a, FrontPort):
            kwargs_a = {"front_port": endpoint_a}
        else:
            kwargs_a = {"rear_port": endpoint_a}

        if isinstance(endpoint_b, Interface):
            kwargs_b = {"interface": endpoint_b}
        elif isinstance(endpoint_b, FrontPort):
            kwargs_b = {"front_port": endpoint_b}
        else:
            kwargs_b = {"rear_port": endpoint_b}

        assignment_a = AVPortAssignment.objects.filter(**kwargs_a).select_related("profile").first()
        assignment_b = AVPortAssignment.objects.filter(**kwargs_b).select_related("profile").first()
        if assignment_a is None or assignment_b is None:
            return

        profile_a = assignment_a.profile
        profile_b = assignment_b.profile
        if profile_a.signal != profile_b.signal:
            self.fail(f"AV signal mismatch: {endpoint_a} is {profile_a.get_signal_display()}, {endpoint_b} is {profile_b.get_signal_display()}.")

        if profile_a.rate and profile_b.rate and profile_a.rate != profile_b.rate:
            self.fail(f"AV rate mismatch: {endpoint_a} is {profile_a.get_rate_display()}, {endpoint_b} is {profile_b.get_rate_display()}.")

        if profile_a.connector != profile_b.connector:
            self.fail(f"AV connector mismatch: {endpoint_a} is {profile_a.get_connector_display()}, {endpoint_b} is {profile_b.get_connector_display()}.")

        strict_directions = {
            AVDirectionChoices.DIRECTION_INPUT,
            AVDirectionChoices.DIRECTION_OUTPUT,
        }
        if profile_a.direction == profile_b.direction and profile_a.direction in strict_directions:
            self.fail(f"AV direction mismatch: cannot cable {profile_a.get_direction_display()} to {profile_b.get_direction_display()}.")
