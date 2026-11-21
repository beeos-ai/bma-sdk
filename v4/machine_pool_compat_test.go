package bmasdk_test

import (
	"encoding/json"
	"testing"

	bmasdk "github.com/beeos-ai/bma-sdk/v4"
)

func TestCreateMachinePoolSecretSourceCompatibility(t *testing.T) {
	for _, secret := range []string{"", "sec_aaaaaaaaaaaaaaaaaaaaaaaaaa"} {
		for name, request := range map[string]any{
			"base":    bmasdk.CreateMachinePoolRequestBase{ProviderAuthSecretID: secret},
			"request": bmasdk.CreateMachinePoolRequest{ProviderAuthSecretID: secret},
		} {
			t.Run(name+"/"+secret, func(t *testing.T) {
				data, err := json.Marshal(request)
				if err != nil {
					t.Fatal(err)
				}
				var fields map[string]json.RawMessage
				if err := json.Unmarshal(data, &fields); err != nil {
					t.Fatal(err)
				}
				value, present := fields["provider_auth_secret_id"]
				if present != (secret != "") {
					t.Fatalf("provider_auth_secret_id present = %v: %s", present, data)
				}
				if secret != "" && string(value) != `"`+secret+`"` {
					t.Fatalf("provider_auth_secret_id = %s, want %q", value, secret)
				}
				var decoded bmasdk.CreateMachinePoolRequestBase
				if err := json.Unmarshal(data, &decoded); err != nil {
					t.Fatal(err)
				}
				if decoded.ProviderAuthSecretID != secret {
					t.Fatalf("decoded secret = %q, want %q", decoded.ProviderAuthSecretID, secret)
				}
			})
		}
	}
	// Update still distinguishes omission from setting a value.
	secret := "sec_aaaaaaaaaaaaaaaaaaaaaaaaaa"
	_ = bmasdk.UpdateMachinePoolRequest{ProviderAuthSecretID: &secret}
}

func TestCreateMachinePoolSecretClearedAfterUnmarshal(t *testing.T) {
	var request bmasdk.CreateMachinePoolRequest
	if err := json.Unmarshal([]byte(`{"provider_auth_secret_id":"sec_aaaaaaaaaaaaaaaaaaaaaaaaaa","provider":"fly","name":"pool"}`), &request); err != nil {
		t.Fatal(err)
	}
	if request.ProviderAuthSecretID != "sec_aaaaaaaaaaaaaaaaaaaaaaaaaa" {
		t.Fatalf("decoded secret = %q", request.ProviderAuthSecretID)
	}
	request.ProviderAuthSecretID = ""
	data, err := json.Marshal(request)
	if err != nil {
		t.Fatal(err)
	}
	var fields map[string]json.RawMessage
	if err := json.Unmarshal(data, &fields); err != nil {
		t.Fatal(err)
	}
	if _, present := fields["provider_auth_secret_id"]; present {
		t.Fatalf("cleared secret was retained in union data: %s", data)
	}
	if string(fields["provider"]) != `"fly"` || string(fields["name"]) != `"pool"` {
		t.Fatalf("unrelated union fields changed: %s", data)
	}
}
