from mig_lab.nvidia_mig import parse_smi_l_output


def test_parse_smi_l():
    text = """GPU 0: NVIDIA H200 (UUID: GPU-abc-123)
GPU 1: NVIDIA H200 (UUID: GPU-def-456)
"""
    gpus = parse_smi_l_output(text)
    assert len(gpus) == 2
    assert gpus[0].index == 0
    assert "H200" in gpus[0].name
