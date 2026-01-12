class SpeakTts < Formula
  include Language::Python::Virtualenv

  desc "Voice cloning CLI for Mac using F5-TTS"
  homepage "https://github.com/danielsinai/homebrew-speak-tts"
  url "https://github.com/danielsinai/homebrew-speak-tts/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "a9fcaa20f0d0ed976ff104b2ba259e278d61227112985a043fd475551141acf9"
  license "MIT"

  depends_on "python@3.12"
  depends_on :macos
  depends_on arch: :arm64

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Voice cloning CLI", shell_output("#{bin}/speak --help")
  end
end
