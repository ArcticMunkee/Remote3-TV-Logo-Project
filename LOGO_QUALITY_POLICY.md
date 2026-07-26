# Logo Quality and Scope Policy

- **Policy ID:** `remote3-logo-quality-policy`
- **Version:** 1.0.0
- **Status:** Active
- **Effective date:** 2026-07-26

The machine-readable representation of this policy is
[`logo_quality_policy.json`](logo_quality_policy.json).

## Purpose

This policy governs unattended inspection, selection, cleanup, master promotion,
and output generation for TV channel logos used by the Remote3 TV Logo Project.

The primary goal is high-confidence curation. The pipeline must prefer no result
over a visually plausible but incorrect result.

## Quality contract

- Every candidate is inspected before it can become an approved master.
- Automatic processing is fail-closed.
- Only deterministic and reproducible changes may be approved automatically.
- Raw source files are immutable and are never overwritten.
- Every approved logo has a transparent background.
- Channel identity, market, logo generation, layout, and background variant must
  remain correct.
- Ambiguous or unverifiable candidates are quarantined instead of being forced
  through conversion.
- The pipeline optimizes for precision and brand fidelity, not maximum
  conversion rate.

## Asset lifecycle

### Raw Source

The original bytes obtained from Wikimedia Commons, `tv-logo/tv-logos`, the
existing Remote3 collection, or another approved source.

Raw sources:

- remain unchanged;
- retain their source filename and source identity;
- receive a content hash;
- may be referenced by multiple candidates without being duplicated.

### Master Candidate

A raw source or deterministic derivative that has been classified, inspected,
and compared with other candidates from the same logo family.

### Approved Master

The preferred, verified asset for a specific combination of:

- channel or brand;
- market or region;
- logo generation or validity period;
- layout;
- background compatibility.

An approved master may be a native SVG or a high-quality transparent PNG.
Raster content does not become a vector master merely because it is embedded in
an SVG container.

### Platform Output

A reproducible derivative generated from an approved master for Remote 3, Kodi,
IPTV, Home Assistant, or another supported target.

Platform outputs are not source masters.

## Required classifications

Each candidate must receive:

- an internal asset ID;
- a channel or logo-family identity;
- a format classification;
- a background compatibility classification;
- a processing outcome;
- separate confidence values for semantic identity, technical integrity,
  transformation safety, and visual fidelity.

Public filename normalization is deliberately deferred until the identity and
master-selection model is stable.

## Background compatibility

Approved masters use one of these values:

- `on-light`
- `on-dark`
- `universal`
- `unknown`

Official or source-native light and dark variants are preferred. Full-color
logos must not be inverted automatically. Artificial plates, outlines, or
shadows are treated as derived display variants and not as source masters.

A white logo on a transparent canvas is valid when classified as `on-dark`.

## Allowed unattended operations

An operation may run automatically only after its specific problem has been
detected with sufficient confidence and only when post-processing fidelity
gates are available.

Allowed operations include:

- format validation and safe decoding;
- hash calculation and exact-content deduplication;
- color-profile normalization for platform outputs;
- transparent-canvas normalization;
- removal of an unambiguous border-connected background;
- matte-color estimation and alpha unmatting;
- edge-color decontamination;
- targeted removal of a confirmed border line;
- topology-preserving edge smoothing;
- proportional resizing and target-canvas placement;
- conservative vectorization of simple, sharp, flat-color artwork;
- sanitization of SVGs when rendering equivalence can be demonstrated.

## Prohibited unattended operations

The unattended pipeline must not use:

- image generation;
- generative inpainting;
- semantic or generative super-resolution;
- freehand AI-generated SVG paths;
- guessed reconstruction of cropped or missing shapes;
- automatic replacement of lettering with a similar font;
- global deletion of white, black, or near-white pixels;
- blanket inversion of full-color logos;
- topology-changing smoothing without a verified reference;
- destructive modification of raw source files;
- raster embedding presented as genuine vectorization.

## Hard quality gates

No aggregate score may override a failed hard gate.

### Semantic gate

The asset must be a relevant TV channel or network logo. Channel identity,
market, logo generation, and variant must be sufficiently certain.

### Integrity and safety gate

The file must decode safely within configured resource limits.

SVG candidates must be checked for malformed XML, scripts, event handlers,
external resources, `foreignObject`, unresolved fonts, embedded raster images,
and renderer-dependent behavior.

### Transparency gate

The output canvas must be transparent. A visible white or colored shape may be
removed only when it is demonstrably a canvas background rather than part of
the design.

### Geometry and topology gate

Aspect ratio, silhouette, component count, internal holes, and intended
whitespace must remain valid. New clipping or distortion is prohibited.

### Fidelity gate

Automatic processing must not add, remove, rename, or invent visible logo
elements. Color and edge changes outside the diagnosed repair region must stay
within calibrated tolerances.

### Rendering gate

Candidates must be rendered on white, black, neutral gray, and checkerboard
backgrounds and at representative target sizes.

SVG masters must render consistently with the supported independent renderers.

### Reproducibility gate

The same input, policy version, tool version, and parameters must produce the
same output and decision.

## Processing outcomes

- `approved-original` — the source is approved without visual modification.
- `approved-cleaned` — a deterministic repair passed every applicable gate.
- `needs-better-source` — the candidate cannot meet the quality contract but a
  better authentic source may solve the problem.
- `quarantine-ambiguous` — identity, geometry, background, or transformation is
  not sufficiently certain.
- `manual-reconstruction-required` — information is missing or the artwork is
  unsuitable for unattended reconstruction.

## Replacement policy

An existing project logo may be replaced automatically only when:

- semantic identity is confirmed;
- market, era, layout, and background variant match;
- the proposed master is measurably superior;
- target renderings pass;
- the previous version remains recoverable.

Historical or alternate variants are not defects and must not be silently
discarded.

## Explicitly out of scope

The following are not part of this quality pipeline:

- per-file attribution manifests;
- individual license validation;
- copyright or trademark approval gates;
- public filename normalization before the final normalization phase;
- forced conversion of every candidate;
- speculative manual reconstruction inside the unattended lane.

The repository's existing general asset-rights and trademark notices remain
separate from this policy.

## Change control

Material changes to hard gates, prohibited operations, processing outcomes, or
scope require a policy-version change and regression against the representative
gold set.
