# File Formats


| Feature                   | JSON  | Fix Length | Delimited | Custom Columnar |
|---------------------------|------|------------|-----------|-----------------|
| **Schema Flexibility**    | ✅ High  | ❌ Rigid      | ⚠️ Moderate   | ⚠️ Moderate         |
| **Readability**           | ✅ High  | ✅ High       | ⚠️ Moderate   | ⚠️ Moderate         |
| **Storage Efficiency**    | ❌ Redundant keys | ❌ Inefficient because of padding spaces | ✅ More compact | ✅ Highly compact |
| **Parsing Efficiency**    | ❌ Text-based overhead | ✅ Fast offset-based | ❌ Text-based overhead | ⚠️ Moderate (Optimized for columns) |
| **Metadata Info**         | ✅ Self documenting | ❌ None       | ❌ None       | ❌ None             |
| **Nested Data Support**   | ✅ Full  | ❌ None       | ⚠️ Partial    | ⚠️ Partial          |
| **Query Speed (Row-based)** | ✅ Fast | ✅ Fast | ✅ Fast | ❌ Slow |
| **Query Speed (Column-based)** | ❌ Slow | ❌ Slow | ❌ Slow | ✅ Very Fast |
| **Compression**           | ❌ Inefficient | ❌ Inefficient | ⚠️ Moderate | ✅ High |
| **Type Enforcing**        | ❌ None  | ❌ None       | ❌ None       | ❌ None             |
| **Schema Evolution**      | ✅ Easy  | ❌ Difficult  | ❌ Difficult  | ❌ Difficult        |
| **Adding New Field**  | ✅ Anywhere | ❌ Only at end | ❌ Only at end | ❌ Difficult |
| **Deletion Handling**     | ✅ Easy  | ✅ Easy | ✅ Easy | ❌ Challenging |