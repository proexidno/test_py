pipeline {
    agent any

    environment {
        OBMC_HOST='https://127.0.0.1:2443'
        IPMI_HOST='127.0.0.1'
        IPMI_PORT='2623'
        OBMC_USER=credentials('OBMC_USER')
        OBMC_PASS=credentials('OBMC_PASS')
        IPMI_USER=credentials('IPMI_USER')
        IPMI_PASS=credentials('IPMI_PASS')
    }

    stages {
        stage('Install Qemu') {
            steps {
                sh '''
                    apt-get install -y --update python3 qemu-utils qemu-system-arm python3.13-venv ipmitool wget
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
                    mkdir -p reports
                    python3 -m venv .venv
                    source ./.venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Start OpenBMC in QEMU') {
            steps {
                script {
                    sh '''
                        qemu-system-arm -m 256 -M romulus-bmc -nographic -drive file=./romulus/obmc-phosphor-image-romulus-20250903025632.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &

                        echo $! > qemu.pid
                        sleep 120
                    '''
                }
            }
        }

        stage('Run OpenBMC API Tests') {
            steps {
                sh "pytest tests/api/ -v --junitxml=./reports/pytest.xml --disable-warnings"
            }
            post {
                always {
                    archiveArtifacts artifacts: "reports/pytest.xml", fingerprint: true
                }
            }
        }

        // stage('Driver for WebUI Tests') {
        //     steps {
        //         // This is from official firefox post
        //         sh '''
        //             wget -O geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz"
        //             tar -xzf geckodriver.tar.gz
        //             chmod +x geckodriver
        //             mv geckodriver /usr/local/bin/
        //             '''
        //     }
        // }

        // stage('Run OpenBMC WebUI Tests') {
        //     steps {
        //         sh "python tests/webui/webui-tests.py"
        //     }
        // }

        stage('Run OpenBMC Load Testing') {
            steps {
                sh """
                    mkdir -p reports/locust
                    locust -f tests/locust/locustfile.py \\
                        --headless \\
                        -u 50 \\
                        -r 2 \\
                        --html=./reports/locust/report.html \\
                        --csv=./reports/locust/results \\
                        --run-time 5m \\
                        --exit-code-on-error 1
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: "reports/locust/**", fingerprint: true
                }
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
