package bma

import (
	"context"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"regexp"

	"github.com/beeos-ai/bma-sdk/option"
)

var artifactDigest = regexp.MustCompile(`^sha256:[0-9a-f]{64}$`)

// Download writes artifact content to w after checking it against the size
// and sha256 digest recorded on the artifact. Content larger than maxBytes,
// or than the recorded size, is refused. w receives the bytes as they arrive;
// on error discard what was written.
func (s *AgentArtifactService) Download(ctx context.Context, artifact Artifact, maxBytes int64, w io.Writer, opts ...option.RequestOption) error {
	if maxBytes <= 0 {
		return errors.New("bma: maxBytes is required")
	}
	if artifact.SizeBytes == nil || *artifact.SizeBytes < 0 || *artifact.SizeBytes > maxBytes {
		return errors.New("bma: artifact size is missing or exceeds maxBytes")
	}
	if artifact.Digest == nil || !artifactDigest.MatchString(*artifact.Digest) {
		return errors.New("bma: artifact digest must be sha256:<hex>")
	}
	size := *artifact.SizeBytes
	opts = append([]option.RequestOption{option.WithOrg(artifact.OrgId), option.WithProject(artifact.ProjectId)}, opts...)
	res, err := s.Content(ctx, artifact.AgentId, artifact.Id, opts...)
	if err != nil {
		return err
	}
	defer res.Body.Close()
	hash := sha256.New()
	n, err := io.Copy(io.MultiWriter(w, hash), io.LimitReader(res.Body, size+1))
	if err != nil {
		return fmt.Errorf("bma: read artifact: %w", err)
	}
	if n != size {
		return fmt.Errorf("bma: artifact size = %d, want %d", n, size)
	}
	if subtle.ConstantTimeCompare([]byte("sha256:"+hex.EncodeToString(hash.Sum(nil))), []byte(*artifact.Digest)) != 1 {
		return errors.New("bma: artifact digest mismatch")
	}
	return nil
}
