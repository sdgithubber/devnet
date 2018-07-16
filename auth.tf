provider "google" {
	credentials = "${file("gcp-account.json")}"
	project = "devnet-1"
	region = "us-central-1"
}
