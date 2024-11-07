from enum import Flag, auto, unique


@unique
class PipelineStatus(Flag):
    # --------------------------------------------------- #
    # --- Level 1 Data ---------------------------------- #
    #
    # RAW_SPLITTER --> SPLITTER (Scatter-Gather EIP)
    PROCESSING_RAW_SPLITTER = auto()
    FAILURE_RAW_SPLITTER = auto()
    SUCCESS_RAW_SPLITTER = auto()
    RAW_SPLITTER = PROCESSING_RAW_SPLITTER | FAILURE_RAW_SPLITTER | SUCCESS_RAW_SPLITTER
    #
    # RAW_PROCESSOR --> PROCESSOR (Scatter-Gather EIP)
    PROCESSING_RAW_PROCESSOR = auto()
    FAILURE_RAW_PROCESSOR = auto()
    SUCCESS_RAW_PROCESSOR = auto()
    RAW_PROCESSOR = (
        PROCESSING_RAW_PROCESSOR | FAILURE_RAW_PROCESSOR | SUCCESS_RAW_PROCESSOR
    )
    #
    # RAW_AGGREGATOR --> AGGREGATOR (Scatter-Gather EIP)
    PROCESSING_RAW_AGGREGATOR = auto()
    FAILURE_RAW_AGGREGATOR = auto()
    SUCCESS_RAW_AGGREGATOR = auto()
    RAW_AGGREGATOR = (
        PROCESSING_RAW_AGGREGATOR | FAILURE_RAW_AGGREGATOR | SUCCESS_RAW_AGGREGATOR
    )
    #
    LEVEL_1_PROCESSING = RAW_SPLITTER | RAW_PROCESSOR | RAW_AGGREGATOR
    #
    # TODO: create a comprehensive ENUM of all Failure signals?
    #
    # --------------------------------------------------- #
    # --- Level 2 Data ---------------------------------- #
    #
    # CRUISE_INITIALIZER --> PROCESSOR
    PROCESSING_CRUISE_INITIALIZER = auto()
    FAILURE_CRUISE_INITIALIZER = auto()
    SUCCESS_CRUISE_INITIALIZER = auto()
    CRUISE_INITIALIZER = (
        PROCESSING_CRUISE_INITIALIZER
        | FAILURE_CRUISE_INITIALIZER
        | SUCCESS_CRUISE_INITIALIZER
    )
    #
    # CRUISE_SPLITTER --> SPLITTER
    PROCESSING_CRUISE_SPLITTER = auto()
    FAILURE_CRUISE_SPLITTER = auto()
    SUCCESS_CRUISE_SPLITTER = auto()
    CRUISE_SPLITTER = (
        PROCESSING_CRUISE_SPLITTER | FAILURE_CRUISE_SPLITTER | SUCCESS_CRUISE_SPLITTER
    )
    #
    # CRUISE_PROCESSOR --> PROCESSOR <-- Note: these need to run sequentially now
    PROCESSING_CRUISE_PROCESSOR = auto()
    FAILURE_CRUISE_PROCESSOR = auto()
    SUCCESS_CRUISE_PROCESSOR = auto()
    CRUISE_PROCESSOR = (
        PROCESSING_CRUISE_PROCESSOR
        | FAILURE_CRUISE_PROCESSOR
        | SUCCESS_CRUISE_PROCESSOR
    )
    #
    # CRUISE_AGGREGATOR --> AGGREGATOR
    PROCESSING_CRUISE_AGGREGATOR = auto()
    FAILURE_CRUISE_AGGREGATOR = auto()
    SUCCESS_CRUISE_AGGREGATOR = auto()
    CRUISE_AGGREGATOR = (
        PROCESSING_CRUISE_AGGREGATOR
        | FAILURE_CRUISE_AGGREGATOR
        | SUCCESS_CRUISE_AGGREGATOR
    )
    #
    LEVEL_2_PROCESSING = (
        CRUISE_INITIALIZER | CRUISE_SPLITTER | CRUISE_PROCESSOR | CRUISE_AGGREGATOR
    )
    #
    # --------------------------------------------------- #
    # --- Level 3 Data ---------------------------------- #
    #
    # TILE_PROCESSOR  # TODO: shapefile -> pmtiles -> geohash?
    PROCESSING_TILE_PROCESSOR = auto()
    FAILURE_TILE_PROCESSOR = auto()
    SUCCESS_TILE_PROCESSOR = auto()
    TILE_PROCESSOR = (
        PROCESSING_TILE_PROCESSOR | FAILURE_TILE_PROCESSOR | SUCCESS_TILE_PROCESSOR
    )
    #
    # GEOHASH_PROCESSOR
    PROCESSING_GEOHASH_PROCESSOR = auto()
    FAILURE_GEOHASH_PROCESSOR = auto()
    SUCCESS_GEOHASH_PROCESSOR = auto()
    GEOHASH_PROCESSOR = (
        PROCESSING_GEOHASH_PROCESSOR
        | FAILURE_GEOHASH_PROCESSOR
        | SUCCESS_GEOHASH_PROCESSOR
    )
    #
    LEVEL_3_PROCESSING = TILE_PROCESSOR | GEOHASH_PROCESSOR
    # --------------------------------------------------- #
    # --------------------------------------------------- #


# Status.PROCESSING_RAW_AGGREGATOR in Status.LEVEL_1_PROCESSING
# Status.LEVEL_1_PROCESSING.value < Status.LEVEL_2_PROCESSING.value

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html
"""
CREATE_IN_PROGRESS | CREATE_FAILED | CREATE_COMPLETE |
ROLLBACK_IN_PROGRESS | ROLLBACK_FAILED | ROLLBACK_COMPLETE |
DELETE_IN_PROGRESS | DELETE_FAILED | DELETE_COMPLETE |
UPDATE_IN_PROGRESS | UPDATE_COMPLETE_CLEANUP_IN_PROGRESS | UPDATE_COMPLETE |
UPDATE_FAILED | UPDATE_ROLLBACK_IN_PROGRESS | UPDATE_ROLLBACK_FAILED |
UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS | UPDATE_ROLLBACK_COMPLETE |
REVIEW_IN_PROGRESS | IMPORT_IN_PROGRESS | IMPORT_COMPLETE |
IMPORT_ROLLBACK_IN_PROGRESS | IMPORT_ROLLBACK_FAILED | IMPORT_ROLLBACK_COMPLETE

failure - noun - 
failed - verb - "verbs should be avoided"

success - noun

"""
