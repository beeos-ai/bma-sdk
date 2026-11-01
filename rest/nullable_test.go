package rest_test

import (
	"encoding/json"
	"testing"
	"time"

	bmarest "github.com/beeos-ai/bma-sdks/go/rest"
)

// Nullable contract fields (`anyOf`/`oneOf` with a null branch, whether the
// other branch is a $ref or a base type) are pointers, so null decodes to nil
// and stays distinguishable from a zero value.

func roundTripKey(t *testing.T, value any, key string) json.RawMessage {
	t.Helper()
	raw, err := json.Marshal(value)
	if err != nil {
		t.Fatal(err)
	}
	var fields map[string]json.RawMessage
	if err := json.Unmarshal(raw, &fields); err != nil {
		t.Fatal(err)
	}
	got, ok := fields[key]
	if !ok {
		t.Fatalf("%s missing from marshaled output %s", key, raw)
	}
	return got
}

func TestNullableRefObjectField(t *testing.T) {
	var null bmarest.File
	if err := json.Unmarshal([]byte(`{"id":"file_x","scope":null}`), &null); err != nil {
		t.Fatal(err)
	}
	if null.Scope != nil {
		t.Fatalf("scope: null decoded to %+v, want nil", null.Scope)
	}
	if got := string(roundTripKey(t, null, "scope")); got != "null" {
		t.Fatalf("null scope round-tripped as %s", got)
	}

	var set bmarest.File
	body := `{"id":"file_x","scope":{"type":"session","id":"ses_aaaaaaaaaaaaaaaaaaaaaaaaaa"}}`
	if err := json.Unmarshal([]byte(body), &set); err != nil {
		t.Fatal(err)
	}
	if set.Scope == nil || set.Scope.Id != "ses_aaaaaaaaaaaaaaaaaaaaaaaaaa" {
		t.Fatalf("scope decoded to %+v", set.Scope)
	}
	var want, got any
	_ = json.Unmarshal([]byte(`{"type":"session","id":"ses_aaaaaaaaaaaaaaaaaaaaaaaaaa"}`), &want)
	_ = json.Unmarshal(roundTripKey(t, set, "scope"), &got)
	if !jsonEqual(want, got) {
		t.Fatalf("scope round-tripped as %v", got)
	}
}

func TestNullableRefScalarFields(t *testing.T) {
	var null bmarest.AgentMachine
	if err := json.Unmarshal([]byte(`{"machine_pool_id":null}`), &null); err != nil {
		t.Fatal(err)
	}
	if null.MachinePoolId != nil {
		t.Fatalf("machine_pool_id: null decoded to %q, want nil", *null.MachinePoolId)
	}
	if got := string(roundTripKey(t, null, "machine_pool_id")); got != "null" {
		t.Fatalf("null machine_pool_id round-tripped as %s", got)
	}

	var set bmarest.AgentMachine
	if err := json.Unmarshal([]byte(`{"machine_pool_id":"mpo_abc"}`), &set); err != nil {
		t.Fatal(err)
	}
	if set.MachinePoolId == nil || *set.MachinePoolId != "mpo_abc" {
		t.Fatalf("machine_pool_id decoded to %v", set.MachinePoolId)
	}
	if got := string(roundTripKey(t, set, "machine_pool_id")); got != `"mpo_abc"` {
		t.Fatalf("machine_pool_id round-tripped as %s", got)
	}
}

func TestNullableTimestampField(t *testing.T) {
	var null bmarest.CronTrigger
	if err := json.Unmarshal([]byte(`{"last_fired_at":null,"next_fire_at":null}`), &null); err != nil {
		t.Fatal(err)
	}
	if null.LastFiredAt != nil || null.NextFireAt != nil {
		t.Fatalf("null timestamps decoded to %v, %v", null.LastFiredAt, null.NextFireAt)
	}

	var set bmarest.CronTrigger
	if err := json.Unmarshal([]byte(`{"last_fired_at":"2026-11-01T00:00:00Z"}`), &set); err != nil {
		t.Fatal(err)
	}
	if set.LastFiredAt == nil || !set.LastFiredAt.Equal(time.Date(2026, 11, 1, 0, 0, 0, 0, time.UTC)) {
		t.Fatalf("last_fired_at decoded to %v", set.LastFiredAt)
	}
	if got := string(roundTripKey(t, set, "last_fired_at")); got != `"2026-11-01T00:00:00Z"` {
		t.Fatalf("last_fired_at round-tripped as %s", got)
	}
}

func jsonEqual(a, b any) bool {
	x, _ := json.Marshal(a)
	y, _ := json.Marshal(b)
	return string(x) == string(y)
}
