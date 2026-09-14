# Schema CSV

## frames.csv
- `session_id`: identificativo sessione
- `frame_id`: progressivo frame
- `timestamp_ms`: timestamp millisecondi
- `mirror_mse`, `mpjpe`: metriche per-frame
- `lm_{i}_x`, `lm_{i}_y`, `lm_{i}_vis`, `lm_{i}_conf` per i=0..32 (33 landmark)

## sessions.csv
- `session_id`
- `created_at`: ISO timestamp
- `cam_view`: back/front/side
- `fps`, `width`, `height`: parametri acquisizione

## strides.csv
- `session_id`
- `stride_id`: progressivo stride
- `t_start_ms`, `t_end_ms`: intervallo temporale
- `cadence_spm`: cadenza (step/min)
- `phase_delay_ms`: ritardo di fase (ms)
- `PLV`: phase locking value (0–1)
- `MirrorMSE_mean`, `MPJPE_mean`: medie per stride
- `S_index`: indice di simmetria
- `quality_score`: score composito 0–100
