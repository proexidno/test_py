pipeline {
    agent any

    environment {
        VENV = '.venv'
        PYTHON = '${VENV}/bin/python'
        PYTEST = '${VENV}/bin/pytest'
        LOCUST = '${VENV}/bin/locust'
        QEMU_TIMEOUT_SEC = '600'
    }

    stages {
        stage('Install Qemu') {
            steps {
                sh '''
                    apt-get install -y --update python3 qemu-system-arch
                '''
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    if [ ! -d "${VENV}" ]; then
                        echo "Virtual environment not found. Creating..."
                        python3 -m venv ${VENV}
                        ${VENV}/bin/pip install --upgrade pip
                        ${VENV}/bin/pip install -r requirements.txt
                    else
                        echo "Using existing virtual environment: ${VENV}"
                    fi
                '''
            }
        }

        stage('Start OpenBMC in QEMU') {
            steps {
                script {
                    sh '''
                        timeout ${QEMU_TIMEOUT_SEC} qemu-system-arm -m 256 -M romulus-bmc -nographic -drive file=./romulus/obmc-phosphor-image-romulus-20250903025632.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &

                        echo $! > qemu.pid
                    '''
                }
            }
        }

        stage('Run OpenBMC API Tests') {
            steps {
                sh "${PYTEST} tests/api/ -v"
            }
        }

        stage('Run OpenBMC WebUI Tests') {
            steps {
                sh "${PYTHON} tests/webui/webui-tests.py"
            }
        }

        stage('Run OpenBMC Load Testing') {
            steps {
                sh """
                    ${LOCUST} -f tests/locust/locustfile.py \\
                        --headless \\
                        -u 10 \\
                        -r 2 \\
                        --run-time 2m \\
                        --exit-code-on-error 1
                """
            }
        }
    }

    post {
        always {
            script {
                sh '''
                    if [ -f qemu.pid ]; then
                        PID=$(cat qemu.pid)
                        if kill -0 "$PID" 2>/dev/null; then
                            echo "Stopping QEMU process $PID..."
                            kill "$PID"
                            wait "$PID" 2>/dev/null || true
                        fi
                        rm -f qemu.pid
                    fi
                '''
            }
        }
    }
}
