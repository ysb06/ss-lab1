import subprocess
import re  # 정규 표현식을 사용하기 위해 추가
import os
import time


def run_and_get_output(
    password_guess,
    proc_path="../flush-reload/flush-reload",
    delay=0.032,
):
    proc_dir = os.path.dirname(proc_path)
    if proc_dir == "":
        proc_dir = "."
    proc_name = os.path.basename(proc_path)
    command = [f"./{proc_name}", password_guess]

    time.sleep(delay)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd=proc_dir,
        )
        # Exit code 0 means success - flag found!
        print(f"Debug: Command output:\r\n{result.stdout}")
        return (None, True)  # (output, success)

    except FileNotFoundError:
        print(f"오류: './flush-reload' 파일을 찾을 수 없습니다.")
        return (None, False)
    except subprocess.CalledProcessError as e:
        return (e.stdout, False)  # (output, success)
    except Exception as e:
        print(f"예기치 않은 오류 발생: {e}")
        return (None, False)


def get_time_from_run(
    password_guess,
    proc_path="../flush-reload/flush-reload",
    delay=0.032,
):
    stdout_output, is_success = run_and_get_output(password_guess, proc_path, delay)

    # If password is correct, return special marker
    if is_success:
        return (None, True)  # (time, success)

    if stdout_output:
        match = re.search(r"-> time: (\d+)", stdout_output)

        if match:
            time_str = match.group(1)
            return (int(time_str), False)  # (time, success)
        else:
            print(f"오류: 출력에서 '-> time:' 패턴을 찾을 수 없습니다.")
            print("--- 전체 출력 ---")
            print(stdout_output)
            print("-----------------")
            return (None, False)
    else:
        return (None, False)
