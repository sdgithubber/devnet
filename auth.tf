provider "google" {
	credentials = "${file("gcp-account.json")}"
	project = "spacemesh-198810"
	region = "us-central-1"
}
